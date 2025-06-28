# save_state.py

import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        print("Please log in to France Travail in the browser window...")
        await page.goto("https://authentification-candidat.francetravail.fr/connexion/XUI/?realm=/individu&goto=https://authentification-candidat.francetravail.fr/connexion/oauth2/realms/root/realms/individu/authorize?realm%3D/individu%26response_type%3Did_token%2520token%26scope%3Dactu%2520actuStatut%2520application_USG_PN073-tdbcandidat_6408B42F17FC872440D4FF01BA6BAB16999CD903772C528808D1E6FA2B585CF2%2520compteUsager%2520contexteAuthentification%2520coordonnees%2520courrier%2520email%2520etatcivil%2520idIdentiteExterne%2520idRci%2520individu%2520logW%2520messagerieintegree%2520navigation%2520nomenclature%2520notifications%2520openid%2520pilote%2520pole_emploi%2520prdvl%2520profile%2520reclamation%2520suggestions%2520mesrdvs%2520offre%2520criteresrecherchesoffres%26client_id%3DUSG_PN073-tdbcandidat_6408B42F17FC872440D4FF01BA6BAB16999CD903772C528808D1E6FA2B585CF2%26state%3DQSJx0P1Ba8pauEHl%26nonce%3D0RnH2Uo1Ff5rEuEX%26redirect_uri%3Dhttps://candidat.francetravail.fr/espacepersonnel/#login/")
        await page.pause()
        await context.storage_state(path="auth.json")
        print("Authentication state saved to auth.json")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
