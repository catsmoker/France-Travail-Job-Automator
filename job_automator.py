# job_automator.py - because job hunting sucks and I'm lazy as fuck

import asyncio
import re
import random
from playwright.async_api import async_playwright, TimeoutError

AUTH_FILE = "auth.json"
BASE_URL = "https://candidat.francetravail.fr"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        
        try:
            context = await browser.new_context(storage_state=AUTH_FILE)
            print("✅ Auth loaded, let's fucking go")
        except FileNotFoundError:
            print(f"❌ OH SHIT! '{AUTH_FILE}' not found. Run save_state.py first dumbass")
            await browser.close()
            return

        page = await context.new_page()
        search_url = "https://candidat.francetravail.fr/offres/recherche?motsCles=Saisonnier&offresPartenaires=true&rayon=10&tri=0"
        
        print(f"Going to: {search_url} - cross your fingers...")
        await page.goto(search_url, wait_until='networkidle', timeout=60000)

        processed_job_ids = set()

        while True:
            print("\nLooking for jobs... pray to god...")
            
            all_listings_on_page = await page.locator("li.result").all()
            
            new_listings = []
            for listing in all_listings_on_page:
                job_id = await listing.get_attribute("data-id-offre")
                if job_id and job_id not in processed_job_ids:
                    new_listings.append(listing)
            
            if not new_listings:
                print("Fuck all new jobs. Checking for 'Show More'...")
                list_processed_successfully = True
            else:
                print(f"✅ Found {len(new_listings)} new jobs - time to spam applications!")
                list_processed_successfully = True

                for i, listing in enumerate(new_listings):
                    job_id = await listing.get_attribute("data-id-offre")
                    job_title_text = await listing.locator('h2.media-heading').inner_text()
                    
                    print(f"\n--- Processing Job {job_id}: {job_title_text} ---")
                    processed_job_ids.add(job_id)

                    try:
                        await listing.click()
                        print("  Clicked that shit, waiting...")
                        details_pane = page.locator('div#detailOffreVolet')
                        await details_pane.wait_for(state='visible', timeout=10000)
                    except TimeoutError:
                        print("  ❌ Took too damn long. Skipping.")
                        continue

                    experience_found = False
                    skill_elements = await details_pane.locator(".skill-default > .skill-name").all()
                    
                    if not skill_elements:
                        print("  🟡 No skills? What kinda bullshit job is this?")
                    else:
                        for skill in skill_elements:
                            skill_text = await skill.inner_text()
                            if re.search(r'\d', skill_text):
                                print(f"  ❌ Fuck this 'need {skill_text} years' bullshit. Skipping.")
                                experience_found = True
                                break 
                    
                    if experience_found:
                        print("  Closing this bullshit...")
                        close_button = page.locator("button.modal-details-close").first
                        await close_button.click()
                        await page.wait_for_timeout(random.uniform(1000, 2000))
                        continue
                    
                    print("  ✅ No experience needed! My kinda job! Applying...")
                    apply_url = f"{BASE_URL}/candidature/postulerenligne/{job_id}"
                    print(f"  Going to apply URL: {apply_url}")
                    
                    apply_page = await context.new_page()
                    is_already_applied = False
                    
                    try:
                        await apply_page.goto(apply_url, wait_until='networkidle')
                        
                        try:
                            already_applied_locator = apply_page.locator("button.btn-primary:nth-child(1)")
                            await already_applied_locator.wait_for(state='visible', timeout=3000)
                            print("  🟡 Already applied? Fuck me...")
                            is_already_applied = True
                        except TimeoutError:
                            print("  New application page - let's spam this shit")

                        if not is_already_applied:
                            print("    Clicking checkbox like a mindless drone...")
                            await apply_page.locator(".checkbox > label").click(timeout=10000)
                            
                            print("    Smashing that apply button...")
                            await apply_page.locator(".validation > .btn-primary").click(timeout=10000)

                            print("    🚀 BOOM! Application sent! Eat shit, job market!")
                            await page.wait_for_timeout(random.uniform(3000, 5000))
                        
                    except Exception as e:
                        print(f"    🔥 OH FUCK! Error: {e}")
                    finally:
                        print("  Closing this tab before it crashes...")
                        await apply_page.close()
                        
                        if is_already_applied:
                            print("  Fuck this 'already applied' shit. Reloading...")
                            await page.goto(search_url, wait_until='networkidle')
                            list_processed_successfully = False
                            break
                        else:
                            try:
                                print("  Trying to close this damn modal...")
                                close_button = page.locator("button.modal-details-close").first
                                await close_button.click(timeout=5000)
                                print("  Modal closed. Thank fuck.")
                            except TimeoutError:
                                print("  🟡 Modal won't close? Fuck it, reloading...")
                                await page.goto(search_url, wait_until='networkidle')
                                list_processed_successfully = False
                                break

                    print("  Waiting a sec so they don't ban my ass...")
                    await page.wait_for_timeout(random.uniform(5000, 12000))

            if list_processed_successfully:
                show_more_button_selector = ".results-more > .btn"
                try:
                    show_more_button = page.locator(show_more_button_selector)
                    if await show_more_button.is_visible():
                        print("\n--- Clicking 'Show More' because why the fuck not ---")
                        await show_more_button.click()
                        await page.wait_for_timeout(random.uniform(5000, 8000))
                    else:
                        print("\nNo more jobs? Fuck this, I'm out.")
                        break
                except TimeoutError:
                    print("\n'Show More' button ghosted me. Peace out.")
                    break

        print("\n--- Script Done. Maybe I'll get a job now? Probably not. ---")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
