import os
import pymupdf

pdf_path = "Timeline.docx.pdf"
results_pdf_path = "results_ont.pdf"
output_html = "nanopore_timeline.html"

# Open PDF and extract meaningful timeline images
doc = pymupdf.open(pdf_path)
os.makedirs("images", exist_ok=True)

valid_images = []
for page_num in range(len(doc)):
    page = doc[page_num]
    image_list = page.get_images(full=True)
    for img_idx, img in enumerate(image_list):
        xref = img[0]
        base_image = doc.extract_image(xref)
        if base_image["width"] > 250 and base_image["height"] > 120:
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            img_filename = f"images/p{page_num}_img_{img_idx}.{image_ext}"
            with open(img_filename, "wb") as f:
                f.write(image_bytes)
            valid_images.append(img_filename)

rapid_img = valid_images[0] if len(valid_images) > 0 else ""
rna_img = valid_images[1] if len(valid_images) > 1 else (rapid_img if rapid_img else "")
flow_img = valid_images[2] if len(valid_images) > 2 else (rna_img if rna_img else "")

# Extract Results PDF image
results_img = ""
if os.path.exists(results_pdf_path):
    doc_res = pymupdf.open(results_pdf_path)
    for page_num in range(len(doc_res)):
        page = doc_res[page_num]
        image_list = page.get_images(full=True)
        for img_idx, img in enumerate(image_list):
            xref = img[0]
            base_image = doc_res.extract_image(xref)
            if base_image["width"] > 100 and base_image["height"] > 50:
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                results_img = f"images/results_p{page_num}_img_{img_idx}.{image_ext}"
                with open(results_img, "wb") as f:
                    f.write(image_bytes)
                break
        if results_img:
            break

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nanopore Long-Read Sequencing Use & History</title>
    <style>
        :root {{
            --bg-color: #090d16;
            --surface: #131d31;
            --surface-hover: #1e293b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent: #38bdf8;
            --accent-secondary: #818cf8;
            --accent-gradient: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
            --border: #334155;
            --card-bg: #111827;
        }}
        * {{ box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            line-height: 1.6;
            margin: 0;
            padding: 0;
        }}
        header {{
            background: linear-gradient(180deg, #1e293b 0%, #090d16 100%);
            border-bottom: 1px solid var(--border);
            padding: 2.5rem 2rem 1.5rem 2rem;
            text-align: center;
        }}
        h1 {{
            font-size: 2.25rem;
            margin: 0 0 0.5rem 0;
            background: var(--accent-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.025em;
        }}
        .author {{ color: var(--text-muted); font-size: 1.05rem; }}
        .ai-credit {{ color: var(--accent-secondary); font-size: 0.85rem; margin-top: 4px; }}
        header p {{ color: var(--text-muted); font-size: 1rem; max-width: 700px; margin: 0.5rem auto 0 auto; }}
        
        .nav-container {{
            display: flex;
            justify-content: center;
            gap: 0.5rem;
            background: var(--surface);
            padding: 0.75rem 1rem;
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            z-index: 100;
            backdrop-filter: blur(8px);
            flex-wrap: wrap;
        }}
        .tab-btn {{
            background: transparent;
            border: 1px solid var(--border);
            color: var(--text-muted);
            padding: 0.55rem 1.1rem;
            border-radius: 0.5rem;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.9rem;
            transition: all 0.2s ease;
        }}
        .tab-btn:hover, .tab-btn.active {{
            background: var(--accent);
            color: #090d16;
            border-color: var(--accent);
            box-shadow: 0 0 15px rgba(56, 189, 248, 0.3);
        }}

        .main-container {{
            max-width: 960px;
            margin: 2.5rem auto;
            padding: 0 1.5rem;
        }}
        .tab-content {{ display: none; animation: fadeIn 0.3s ease-in-out; }}
        .tab-content.active {{ display: block; }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: translateY(0); }} }}

        h2 {{ font-size: 1.8rem; color: var(--accent); margin-bottom: 1rem; border-bottom: 2px solid var(--border); padding-bottom: 0.5rem; }}
        h3 {{ color: var(--text-main); margin-top: 1.5rem; }}
        p, li {{ color: var(--text-muted); font-size: 1.05rem; }}

        .card {{
            background-color: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 1rem;
            padding: 2rem;
            margin: 1.5rem 0;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        }}

        .img-card {{
            background-color: #ffffff;
            border: 1px solid var(--border);
            border-radius: 1rem;
            padding: 1.5rem;
            margin: 1.5rem 0;
            text-align: center;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
        }}
        .img-card img {{ max-width: 100%; height: auto; border-radius: 0.5rem; }}
        .img-card p {{ color: #475569; font-style: italic; margin-top: 1rem; margin-bottom: 0; font-weight: 500; }}

        /* Accordions & Timeline Milestones */
        .accordion {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 0.75rem;
            margin: 1rem 0;
            overflow: hidden;
        }}
        .accordion-header {{
            padding: 1.25rem;
            cursor: pointer;
            font-weight: 600;
            color: var(--text-main);
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(255,255,255,0.02);
        }}
        .accordion-header:hover {{ background: rgba(56, 189, 248, 0.05); }}
        .accordion-body {{
            padding: 0 1.25rem 1.25rem 1.25rem;
            display: none;
            border-top: 1px solid var(--border);
        }}
        .accordion.open .accordion-body {{ display: block; padding-top: 1rem; }}

        /* Timeline Styles for Tab 1 */
        .timeline-container {{
            position: relative;
            margin-top: 1.5rem;
        }}
        .timeline-container::before {{
            content: '';
            position: absolute;
            left: 20px;
            top: 0;
            bottom: 0;
            width: 4px;
            background: var(--border);
        }}
        .milestone {{
            position: relative;
            margin-bottom: 2rem;
            margin-left: 55px;
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px 25px;
            cursor: pointer;
            transition: transform 0.2s ease, border-color 0.2s ease;
        }}
        .milestone:hover {{
            transform: translateY(-2px);
            border-color: var(--accent);
        }}
        .milestone::before {{
            content: '';
            position: absolute;
            left: -43px;
            top: 22px;
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: var(--accent);
            border: 3px solid var(--bg-color);
        }}
        .year {{
            font-size: 0.9rem;
            font-weight: bold;
            color: var(--accent);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 5px;
        }}
        .milestone-title {{
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 10px;
            color: var(--text-main);
        }}
        .milestone-details {{
            font-size: 0.95rem;
            color: var(--text-muted);
            line-height: 1.6;
            display: none;
            margin-top: 15px;
            border-top: 1px solid var(--border);
            padding-top: 15px;
        }}
        .milestone.active .milestone-details {{ display: block; }}
        .media-box {{
            margin-top: 15px;
            background: #0f172a;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 15px;
            text-align: center;
        }}
        .media-box img {{ max-width: 100%; height: auto; border-radius: 6px; margin-bottom: 10px; border: 1px solid var(--border); background: #ffffff; }}
        .data-table {{
            width: 100%;
            margin: 15px 0;
            border-collapse: collapse;
            font-size: 0.85rem;
            text-align: left;
            color: var(--text-main);
        }}
        .data-table th, .data-table td {{ border: 1px solid var(--border); padding: 8px 12px; }}
        .data-table th {{ background-color: #0f172a; color: var(--accent); }}
        .references {{ margin-top: 12px; font-size: 0.85rem; color: var(--accent); }}
        .references a, .references div {{ color: var(--accent); text-decoration: underline; display: block; margin-top: 4px; }}
        .references div {{ text-decoration: none; color: var(--text-muted); }}
        .hint {{ font-size: 0.8rem; color: var(--accent-secondary); margin-top: 10px; font-style: italic; }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            background-color: var(--card-bg);
            border-radius: 1rem;
            overflow: hidden;
            border: 1px solid var(--border);
        }}
        th, td {{ padding: 1.25rem; text-align: left; border-bottom: 1px solid var(--border); vertical-align: top; }}
        th {{ background-color: rgba(56, 189, 248, 0.1); color: var(--accent); font-weight: 600; }}
        tr:last-child td {{ border-bottom: none; }}

        .unpublished-note {{
            margin-top: 2rem;
            padding: 1rem;
            background: rgba(56, 189, 248, 0.05);
            border-left: 4px solid var(--accent);
            border-radius: 0.5rem;
            font-style: italic;
            color: var(--accent-secondary);
        }}

        footer {{
            margin-top: 4rem;
            border-top: 1px solid var(--border);
            padding: 2.5rem 1.5rem;
            background: var(--surface);
            font-size: 0.9rem;
            color: var(--text-muted);
        }}
        footer ul {{ padding-left: 1.25rem; }}
        footer li {{ margin-bottom: 0.5rem; }}
        a {{ color: var(--accent); text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>

    <header>
        <h1>Nanopore Long-Read Sequencing Use & History</h1>
        <div class="author">Author and Creator: Brianna Sapounas</div>
        <div class="ai-credit">AI Statement: Google Gemini was used to structure the interactive dashboard</div>
        <p>Interactive platform covering historical evolution, protocols, preparation timelines, mechanisms, and comparative workflows.</p>
    </header>

    <div class="nav-container">
        <button class="tab-btn active" onclick="switchTab(event, 'history')">History & Evolution</button>
        <button class="tab-btn" onclick="switchTab(event, 'overview')">Overview & Scope</button>
        <button class="tab-btn" onclick="switchTab(event, 'protocols')">Workflows & Protocols</button>
        <button class="tab-btn" onclick="switchTab(event, 'mechanism')">Flow Cell & Mechanism</button>
        <button class="tab-btn" onclick="switchTab(event, 'comparison')">Pros & Cons</button>
        <button class="tab-btn" onclick="switchTab(event, 'results')">Results</button>
        <button class="tab-btn" onclick="switchTab(event, 'references')">References</button>
    </div>

    <div class="main-container">

        <!-- TAB 1: HISTORY -->
        <div id="history" class="tab-content active">
            <h2>The Evolution of Epigenetic & Nanopore Sequencing</h2>
            <p style="color: var(--text-muted); margin-bottom: 1.5rem;">Click any milestone card below to expand historical details, figures, tables, and clickable references.</p>
            <div class="timeline-container" id="timeline"></div>
        </div>

        <!-- TAB 2: OVERVIEW -->
        <div id="overview" class="tab-content">
            <h2>Overview & Scope</h2>
            <div class="card">
                <h3>Method & Protocol Preparation Time</h3>
                <p>Total preparation time for nanopore long-read sequencing varies depending on the targeted nucleic acid molecule type:</p>
                <ul>
                    <li><strong>DNA:</strong> Ranges from 10 min (Rapid Sequencing Kit) up to 3 hours 20 min with an overnight incubation period (Ultra-long DNA Sequencing Kit).</li>
                    <li><strong>RNA:</strong> Ranges between 2 hours 20 min (Direct RNA Sequencing Kit) and 3 hours 45 min + PCR time (cDNA-PCR Sequencing Kit).</li>
                </ul>
            </div>

            <div class="card">
                <h3>Main Types of Sequencing</h3>
                <ul>
                    <li><strong>Indirect:</strong> Involves PCR amplification; results in the loss of modified basecalling ability.</li>
                    <li><strong>Direct:</strong> No PCR amplification required; successfully retains modified basecalling data.</li>
                </ul>
            </div>

            <div class="card">
                <h3>What Can You Sequence?</h3>
                <p>Just about any sized DNA or RNA molecule (~20 bp to 4 Mb)! Any organism's nucleic material can be analyzed, as basecalling can be performed with alignment to a reference genome or <em>de novo</em> without alignment.</p>
            </div>
        </div>

        <!-- TAB 3: PROTOCOLS -->
        <div id="protocols" class="tab-content">
            <h2>Workflows & Protocol Guides</h2>
            <p>Click below to inspect the step-by-step library preparation protocols.</p>

            <div class="accordion open" onclick="toggleAccordion(this)">
                <div class="accordion-header">
                    <span>Rapid Sequencing Kit Workflow (DNA)</span>
                    <span>&#9660;</span>
                </div>
                <div class="accordion-body">
                    <p>Uses a transposome complex for rapid gDNA cleavage and simultaneous adapter tagging in roughly 5 minutes, followed by 15 minutes for sequencing adapter attachment.</p>
                    <div class="img-card">
                        <img src="{rapid_img}" alt="Rapid Sequencing Kit Workflow">
                        <p>Rapid Sequencing Kit Workflow Diagram</p>
                    </div>
                </div>
            </div>

            <div class="accordion" onclick="toggleAccordion(this)">
                <div class="accordion-header">
                    <span>Direct RNA Sequencing Kit Workflow</span>
                    <span>&#9660;</span>
                </div>
                <div class="accordion-body">
                    <p>Poly(A) RNA annealing and reverse transcription adapter ligation (~85 min) enabling direct long-read transcript analysis without cDNA conversion bias.</p>
                    <div class="img-card">
                        <img src="{rna_img}" alt="Direct RNA Sequencing Workflow">
                        <p>Direct RNA Sequencing Kit Workflow Diagram</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 4: MECHANISM -->
        <div id="mechanism" class="tab-content">
            <h2>Mechanism & Flow Cell Reader</h2>
            <div class="card">
                <h3>How Nanopore Sequencing Works</h3>
                <p>Each kit utilizes specific reagents, but all depend on motor proteins threading nucleic acids through biological nanopores embedded in an electrically resistant membrane. Current disruptions create characteristic "squiggles" corresponding to specific nucleotide k-mers.</p>
                <div class="img-card">
                    <img src="{flow_img}" alt="Flow Cell Squiggle Reader">
                    <p>Flow Cell Reader & Squiggle Evaluation</p>
                </div>
            </div>
        </div>

        <!-- TAB 5: COMPARISON -->
        <div id="comparison" class="tab-content">
            <h2>Comparative Overview</h2>
            <table>
                <thead>
                    <tr>
                        <th>Nanopore Long-Read Sequencing Advantages</th>
                        <th>Nanopore Long-Read Sequencing Disadvantages</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>
                            <ul>
                                <li>Ultra-long read capability with tunable selectivity</li>
                                <li>Versatile: DNA/RNA/modifications (soon polypeptides?)</li>
                                <li>Reusable flow cell with portable/user-friendly device</li>
                                <li>Greater yield return with faster/simpler library preparation</li>
                            </ul>
                        </td>
                        <td>
                            <ul>
                                <li>Lowered basecall accuracy (91-98.7%)</li>
                                <li>Rapid technological advancements that require continuous updates</li>
                                <li>Large raw data file sizes (total > 1.0 TB)</li>
                                <li>Flow cell pore availability variables</li>
                            </ul>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- TAB 6: RESULTS -->
        <div id="results" class="tab-content">
            <h2>Results & Experimental Data</h2>
            <div class="card">
                <h3>ONT in Action: Coverage of the Clamp Locus</h3>
                <p>Analysis of direct long-read sequencing metrics and coverage across <em>clamp</em> isoforms (clamp-RB and clamp-RA) in wild-type and mutant samples.</p>
                
                {f'''<div class="img-card">
                    <img src="{results_img}" alt="ONT in Action Coverage of Clamp Locus">
                    <p>Coverage of clamp locus across Female yw, Male yw, Female delP/6Q, and Male delP/6Q</p>
                </div>''' if results_img else '<p style="color:var(--accent-secondary);">[Coverage image not found or loaded]</p>'}

                <h3>Sequencing Metrics Summary</h3>
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Metric</th>
                            <th>Female yw</th>
                            <th>Male yw</th>
                            <th>Female delP/6Q</th>
                            <th>Male delP/6Q</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Total reads sequenced</td>
                            <td>18,804,822</td>
                            <td>16,100,000</td>
                            <td>14,403,704</td>
                            <td>16,355,528</td>
                        </tr>
                        <tr>
                            <td>Longest isoform sequenced (nt)</td>
                            <td>422,662</td>
                            <td>401,979</td>
                            <td>343,392</td>
                            <td>461,129</td>
                        </tr>
                        <tr>
                            <td>Median read quality</td>
                            <td>19.3</td>
                            <td>20.1</td>
                            <td>19.9</td>
                            <td>20</td>
                        </tr>
                        <tr>
                            <td>Read length (n50)</td>
                            <td>1,274</td>
                            <td>1,299.00</td>
                            <td>1,298.00</td>
                            <td>1,281.00</td>
                        </tr>
                        <tr>
                            <td>Total assigned reads</td>
                            <td>15,585,239</td>
                            <td>13,074,641</td>
                            <td>11,759,018</td>
                            <td>12,082,762</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="unpublished-note">
                Note: This is unpublished data.
            </div>
        </div>

        <!-- TAB 7: REFERENCES -->
        <div id="references" class="tab-content">
            <h2>References</h2>
            <div class="card">
                <ul>
                    <li>Oxford Nanopore Technologies Documents: <a href="https://nanoporetech.com/resources/document-repository" target="_blank">Document Repository</a></li>
                    <li id="ref-1">1. Jain et al., <em>Nat. Biotechnol.</em>, 2018: <a href="https://doi.org/10.1038/nbt.4060" target="_blank">doi.org/10.1038/nbt.4060</a></li>
                    <li id="ref-2">2. Loose et al., <em>Nat. Methods</em>, 2016: <a href="https://doi.org/10.1038/nmeth.3930" target="_blank">doi.org/10.1038/nmeth.3930</a></li>
                    <li id="ref-3">3. Akeson et al., US Patent #: US 11,970,738 B2, 2024: <a href="https://patentimages.storage.googleapis.com/99/36/59/5146a1db78a52c/US11970738.pdf" target="_blank">Patent PDF</a></li>
                    <li id="ref-4">4. ONT Documents: <a href="https://nanoporetech.com/resources/document-repository?filter.content-type=documentType%3EMethodology+documentation&filter.content-type=documentType%3EWorkflow" target="_blank">Methodology & Workflow Documentation</a></li>
                    <li id="ref-5">5. Klier, Master's Projects, 2022: <a href="https://doi.org/10.31979/etd.n6cs-f4jw" target="_blank">doi.org/10.31979/etd.n6cs-f4jw</a></li>
                    <li id="ref-6">6. Santos et al., <em>Int. J. Mol. Sci.</em>, 2025: <a href="https://doi.org/10.3390/ijms26104492" target="_blank">doi.org/10.3390/ijms26104492</a></li>
                    <li id="ref-7">7. Jayasooriya et al., <em>Genome Res.</em>, 2025: <a href="https://doi.org/10.1101/gr.280090.124" target="_blank">doi.org/10.1101/gr.280090.124</a></li>
                </ul>
            </div>
        </div>

    </div>

    <script>
        // Timeline Data Injection
        const historyData = [
            {{
                year: "1965",
                title: "RNA Sequencing & Early Modification Detection",
                desc: "Utilizing direct yeast tRNA as the model organism, early analytical methodology relied on enzymatic digestion to fragment RNA into overlapping oligonucleotides. These fragments were subsequently separated based on molecular weight and electric charge. While data processing required 2.5 years of manual calculations, this foundational procedure successfully resolved fractions up to 77 nucleotides in length and enabled the detection of specific modified bases.",
                images: ["image_p1_1.png", "image_p1_2.png"],
                tableHtml: `
                    <table class="data-table">
                        <caption>TABLE II: Identities of trinucleotide peaks in Fig. 3 (Tube numbers correspond to Fig. 3)</caption>
                        <thead>
                            <tr><th>Tube No.</th><th>Composition of peak</th></tr>
                        </thead>
                        <tbody>
                            <tr><td>109-115</td><td>1-MeGpGpCp / ApGpCp</td></tr>
                            <tr><td>118-125</td><td>ApGpDiHUp</td></tr>
                            <tr><td>140-148</td><td>GpApUp</td></tr>
                            <tr><td>153-159</td><td>GpGpDiHUp</td></tr>
                            <tr><td>160-170</td><td>IpGpCp / GpGpTp</td></tr>
                        </tbody>
                    </table>
                `,
                refs: [
                    {{ text: "Reference: Holley et al., The Journal of Biological Chemistry, 1965", url: "https://www.jbc.org/article/S0021-9258(18)97435-1/pdf", isText: false }}
                ]
            }},
            {{
                year: "1977",
                title: "DNA Sanger Sequencing including Modification sequencing",
                desc: "Focusing on the bacteriophage genome (5,386 nt) using cDNA templates, this milestone marked the sequencing of the first complete genome. The protocol utilized chain-terminating modified nucleotides, restriction enzyme digestion, chromatography, and electrophoresis. Although requiring several years of experimental execution, it established the cornerstone for sequence-based molecular biology.",
                images: ["image_p3_1.jpeg", "image_p3_2.png"],
                tableHtml: "",
                refs: [
                    {{ text: "References: Sanger et al., Proc. Natl. Acad. Sci., 1977", url: "https://doi.org/10.1073/pnas.74.12.5463", isText: false }},
                    {{ text: "Schroeder K., A History of Sequencing, 2022", url: "https://frontlinegenomics.com/a-history-of-sequencing/", isText: false }}
                ]
            }},
            {{
                year: "1987",
                title: "Sanger Sequencing Commercialized (ABI 370A)",
                desc: "The commercialization of automated Sanger sequencing via the ABI 370A platform streamlined DNA and cDNA analysis up to 400 base pairs per 5-hour run. The system employed fluorescently labeled inhibitory ddNTPs coupled with laser-induced detection to generate high-resolution chromatograms. While maintaining exceptionally high analytical accuracy and serving extensively for specialized assays such as bisulfite sequencing, it remains economically prohibitive for large-scale high-throughput projects.",
                images: ["image_p4_1.jpeg", "image_p5_1.jpeg", "image_p5_2.png"],
                tableHtml: "",
                refs: [
                    {{ text: "Applied Biosystems 370A Prototype Automated DNA Gene Sequencer, Science Museum Group Collection", url: "https://collection.sciencemuseumgroup.org.uk/objects/co61227/prototype-automated-dna-gene-sequencer", isText: false }},
                    {{ text: "Ansorge et al., Nucleic Acids Research, 1987", url: "https://doi.org/10.1093/nar/15.11.4593", isText: false }},
                    {{ text: "Sanger Sequencing Steps & Method, Millipore Sigma", url: "https://www.sigmaaldrich.com/US/en/technical-documents/protocol/genomics/sequencing/sanger-sequencing", isText: false }}
                ]
            }},
            {{
                year: "1989",
                title: "Nanopore sequencing as a theory",
                desc: "Professor David Deamer formulated the theoretical premise that integrating a biological protein channel into an amphiphilic membrane could spatially accommodate individual nucleotides of a translocating DNA strand. It was hypothesized that the resulting modulations in ionic current during translocation could be measured to determine primary base identity.",
                images: ["image_p6_1.jpeg"],
                tableHtml: "",
                refs: [
                    {{ text: "Reference: Oxford Nanopore Technologies History", url: "https://nanoporetech.com/about/history#The-early-years", isText: false }}
                ]
            }},
            {{
                year: "1996",
                title: "First experiments on nanopore technology",
                desc: "Utilizing <i>Staphylococcus aureus</i> &alpha;-hemolysin as the model system, researchers experimentally demonstrated that single-stranded DNA and RNA molecules could be electrophoretically driven through the protein channel via an applied ionic current. These initial recordings confirmed that polymer translocation generates characteristic current blockades, yielding critical quantitative insights into translocation velocity and molecular dynamics.",
                images: ["image_p7_1.png"],
                tableHtml: "",
                refs: [
                    {{ text: "Reference: Kasianowicz et al., PNAS, 1996", url: "https://doi.org/10.1073/pnas.93.24.13770", isText: false }}
                ]
            }},
            {{
                year: "1998",
                title: "First patent granted US Patent 5,795,782",
                desc: "Issuance of a landmark foundational patent for characterizing linear polymers and nucleic acids based on monitoring monomer-interface interactions and characteristic ionic current blockades as molecules traverse nanoscale pores.",
                images: ["image_p8_1.png"],
                tableHtml: "",
                refs: [
                    {{ text: "Reference: US Patent 5,795,782 (USPTO)", url: "https://patents.google.com/patent/US5795782A/en", isText: false }}
                ]
            }},
            {{
                year: "2011",
                title: "PacBio SMRT Sequencing",
                desc: "Pacific Biosciences introduced Single Molecule Real-Time (SMRT) long-read DNA sequencing with inherent capacity for epigenetic modification detection. Operating with average read lengths of 1 to 2.5 kb (capturing fragments up to 10 kb) across 3-hour runs yielding 35,000 to 50,000 high-accuracy reads, the technology relies on phospholinked fluorescent dNTP incorporation kinetics monitored continuously by immobilized polymerases.",
                images: ["image_p9_1.jpeg"],
                tableHtml: "",
                refs: [
                    {{ text: "Coupland et al., BioTechniques, 2013", url: "https://doi.org/10.2144/000113962", isText: false }},
                    {{ text: "Logsdon et al., Nat. Rev. Genet., 2020", url: "https://doi.org/10.1038/s41576-020-0236-x", isText: false }}
                ]
            }},
            {{
                year: "2014",
                title: "MinION and PromethION become available",
                desc: "Oxford Nanopore Technologies introduced portable and high-throughput sequencing systems capable of read lengths exceeding 150 kilobases alongside native C-5 cytosine epigenetic modification profiling (including 5-mC, 5-hmC, 5-fC, and 5-caC). Supporting full-length cDNA sequencing for transcriptome resolution, simultaneous genomic alignment, and real-time target enrichment, standard runs generate 2 to 5 million reads over 48 hours. Both MinION and PromethION platforms are actively maintained at UMass Boston.",
                images: ["image_p10_1.jpeg", "image_p11_1.jpeg"],
                tableHtml: "",
                refs: [
                    {{ text: "Jain et al., Genome Biol., 2016", url: "https://doi.org/10.1186/s13059-016-1122-x", isText: false }},
                    {{ text: "Oxford Nanopore Technologies Store", url: "https://store.nanoporetech.com/us/", isText: false }}
                ]
            }},
            {{
                year: "2017",
                title: "Direct RNA sequencing",
                desc: "The deployment of direct RNA long-read sequencing eliminated reverse transcription artifacts and PCR amplification bias entirely, enabling direct transcriptome quantification with molecule-specific accuracy across at least 16 distinct RNA modification types. Sequencing runs yield 20 to 30 million reads over 24 to 72 hours, with typical read lengths spanning 600 nucleotides to 2.5 kb (and maximal captures up to 15 to 30 kb). The 2019 release of flow-cell wash kits further optimized experimental workflows by enabling consecutive multiplexed reuse of individual flow cells.",
                images: ["image_p12_1.jpeg", "image_p12_2.png"],
                tableHtml: "",
                refs: [
                    {{ text: "Geralde et al., Nat. Methods, 2018", url: "https://doi.org/10.1038/nmeth.4577", isText: false }},
                    {{ text: "Lin et al., Nucleic Acids Research, 2025", url: "https://doi.org/10.1093/nar/gkaf1144", isText: false }},
                    {{ text: "Created with BioRender.com", url: "", isText: true }}
                ]
            }}
        ];

        const timelineContainer = document.getElementById('timeline');
        historyData.forEach((item, index) => {{
            const div = document.createElement('div');
            div.className = 'milestone' + (index === 0 ? ' active' : '');
            
            let imagesHtml = '';
            item.images.forEach(img => {{
                imagesHtml += `<img src="${{img}}" alt="Figure for ${{item.year}}" onerror="this.style.display='none';">`;
            }});

            let refsHtml = '';
            item.refs.forEach(ref => {{
                if (ref.isText) {{
                    refsHtml += `<div>${{ref.text}}</div>`;
                }} else {{
                    refsHtml += `<a href="${{ref.url}}" target="_blank">${{ref.text}}</a>`;
                }}
            }});

            div.innerHTML = `
                <div class="year">${{item.year}}</div>
                <div class="milestone-title">${{item.title}}</div>
                <div class="milosphere-details" style="display:none;"></div>
                <div class="milestone-details">
                    <div>${{item.desc}}</div>
                    ${{item.tableHtml}}
                    ${{imagesHtml ? `<div class="media-box">${{imagesHtml}}</div>` : ''}}
                    <div class="references">${{refsHtml}}</div>
                </div>
                <div class="hint">Click to toggle details, figures, tables & references</div>
            `;
            div.addEventListener('click', () => {{
                div.classList.toggle('active');
            }});
            timelineContainer.appendChild(div);
        }});

        function switchTab(evt, tabName) {{
            const contents = document.querySelectorAll('.tab-content');
            contents.forEach(c => c.classList.remove('active'));

            const buttons = document.querySelectorAll('.tab-btn');
            buttons.forEach(b => b.classList.remove('active'));

            document.getElementById(tabName).classList.add('active');
            evt.currentTarget.classList.add('active');
        }}

        function toggleAccordion(element) {{
            element.classList.toggle('open');
        }}
    </script>
</body>
</html>
"""

with open(output_html, "w") as f:
    f.write(html_content)

print(f"Successfully generated {output_html} with clean results and no citations!")
