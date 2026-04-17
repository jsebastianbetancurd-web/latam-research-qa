import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

DOCS = [
    {"filename": "Latam_Rates_Strategy_Q1.pdf", "desk": "Rates", "country": "LATAM", "content": "Our outlook on Latam rates indicates that Brazil's Selic will remain restrictive to combat core inflation, while Chile's TPM might see aggressive cuts before mid-year. Colombia's Banrep will maintain a cautious pace of 50 bps cuts given fiscal risks."},
    {"filename": "MXN_FX_Volatility_Alert.pdf", "desk": "FX", "country": "MX", "content": "The Mexican Peso (MXN) continues to benefit from nearshoring FDI and high carry. Banxico's recent board minutes suggest a pause in rate cuts, which should keep USD/MXN anchored near 16.50 over the next quarter."},
    {"filename": "BRL_Credit_Corporate_Defaults.pdf", "desk": "Credit", "country": "BR", "content": "Brazilian corporate credit markets face turbulence as refinancing walls approach. Retail sectors are particularly vulnerable if the Selic rate doesn't drop below single digits next year."},
    {"filename": "COP_USD_Intervention_Risks.pdf", "desk": "FX", "country": "CO", "content": "USD/COP volatility has spiked. We see intervention risk if the pair crosses 4,100, though Banrep usually prefers allowing free-floating adjustments. Fiscal deficit widening is a primary driver for the currency weakness."},
    {"filename": "Chile_Sovereign_Bonds_Upgrade.pdf", "desk": "Rates", "country": "CL", "content": "Chile's sovereign curve presents a buying opportunity at the long end. If copper prices stabilize, fiscal revenues will improve, creating an environment for spread compression vs US Treasuries."},
    {"filename": "Peru_Pen_Stability_Report.pdf", "desk": "FX", "country": "PE", "content": "The Peruvian Sol (PEN) remains one of the most stable currencies in the region. BCRP's active intervention strategy and ample FX reserves provide a strong cushion against external shocks."},
    {"filename": "Latam_Equities_Rotation.pdf", "desk": "Equities", "country": "LATAM", "content": "We recommend a rotation from Mexican industrials into Brazilian financials. Valuations in Bovespa look extremely cheap compared to historical averages, assuming the fiscal target isn't heavily modified."},
    {"filename": "Mexico_Elections_Impact.pdf", "desk": "All", "country": "MX", "content": "Upcoming elections in Mexico generate tail risks for local markets. While the frontrunner promises continuity, any supermajority in Congress could revive constitutional reforms affecting autonomous institutions."},
    {"filename": "Colombia_Pension_Reform_Credit.pdf", "desk": "Credit", "country": "CO", "content": "The proposed pension reform in Colombia could severely impact local capital markets. Shifting flows from private AFPs to the public system (Colpensiones) would drain liquidity from local corporate bonds (TES and private debt)."},
    {"filename": "Brazil_Copom_Meeting_Notes.pdf", "desk": "Rates", "country": "BR", "content": "Notes from yesterday's Copom meeting: The split 5-4 vote on the 25bps cut indicates a divided board. We expect the terminal rate to settle higher than market consensus, hovering around 10.50%."},
    {"filename": "Latam_Derivatives_Swaps_Pricing.pdf", "desk": "Derivatives", "country": "LATAM", "content": "TIIE swaps in Mexico are currently pricing in only 3 cuts this year, down from 6 in January. In Brazil, DI futures curve has significantly steepened reflecting fiscal deterioration premium."},
    {"filename": "Chile_Lithium_Strategy_Update.pdf", "desk": "Credit", "country": "CL", "content": "The National Lithium Strategy creates joint venture opportunities but with state majority control. This ambiguity slightly increases funding costs for mining sector corporates trying to issue green bonds."},
    {"filename": "Peru_Pension_Withdrawals_Impact.pdf", "desk": "Rates", "country": "PE", "content": "A 7th round of AFP pension withdrawals has been approved. The BCRP will likely have to provide liquidity facilities again to prevent massive fire sales of sovereign bonds in the secondary market."},
    {"filename": "Argentina_FX_Devaluation_Ripple.pdf", "desk": "FX", "country": "AR", "content": "While Argentina remains largely segmented, further sharp devaluations of the official FX rate could marginally impact Brazilian export competitiveness in the auto sector."},
    {"filename": "Latam_Green_Bond_Issuance.pdf", "desk": "Credit", "country": "LATAM", "content": "ESG-linked corporate bond issuance in Latam surged 20% YoY. Chilean and Brazilian utilites lead the volume. Greeniums are compressing, but institutional demand in Europe remains solid for Latam paper."},
    {"filename": "Mexico_Banxico_Terminal_Rate_Call.pdf", "desk": "Rates", "country": "MX", "content": "We are revising our Banxico terminal rate call to 10.00% by year-end. Services inflation is proving stickier than expected, justifying the central bank's hawkish tone in recent communiques."},
    {"filename": "Brazil_Tax_Reform_Memos.pdf", "desk": "All", "country": "BR", "content": "The consumption tax reform (IVA) in Brazil will take years to fully implement, but the immediate transition rules will squeeze margins for the service sector while benefiting capital goods manufacturing."},
    {"filename": "Colombia_Fiscal_Rule_Concerns.pdf", "desk": "Rates", "country": "CO", "content": "Missing the fiscal rule target in Colombia would prompt a downgrade. Local TES yields have already started pricing in a risk premium of 70 bps over external factors."},
    {"filename": "Chile_TPM_Aggression_Summary.pdf", "desk": "Rates", "country": "CL", "content": "The Central Bank of Chile (BCCh) shocked markets with a 100 bps cut. The accompanying statement suggests rapid normalization to neutral. Short-end rates present a strong receive opportunity."},
    {"filename": "Peru_BCRP_Intervention_Log.pdf", "desk": "FX", "country": "PE", "content": "BCRP intervened three times this week selling USD to tame the PEN depreciation spike. We believe these operations will successfully cap the USD/PEN below 3.85 in the near term."}
]

def generate_pdfs():
    output_dir = "test_docs"
    os.makedirs(output_dir, exist_ok=True)
    
    for doc in DOCS:
        filepath = os.path.join(output_dir, doc["filename"])
        c = canvas.Canvas(filepath, pagesize=letter)
        
        c.setFont("Helvetica-Bold", 16)
        c.drawString(72, 700, f"Citi Internal Research: {doc['filename'].replace('.pdf', '')}")
        
        c.setFont("Helvetica", 12)
        c.drawString(72, 670, f"Target Desk: {doc['desk']}")
        c.drawString(72, 650, f"Country: {doc['country']}")
        c.drawString(72, 630, f"Date: 2024-04-15")
        
        c.setFont("Helvetica", 11)
        text = doc["content"]
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line) + len(word) < 80:
                current_line += word + " "
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)
        
        y = 590
        for line in lines:
            c.drawString(72, y, line)
            y -= 15
            
        c.save()
        print(f"Generated {filepath}")

if __name__ == '__main__':
    print("Generating 20 mock internal strategy PDFs...")
    generate_pdfs()
    print("Done!")
