<!-- Compensation API README.md -->

<!-- Banner -->
<p align="center">
  <img src="https://raw.githubusercontent.com/Emmcrispy/mannysAPI/main/docs/banner.png" alt="Compensation API" width="800"/>
</p>

<h1 align="center">Compensation API</h1>
<p align="center"><em>A production-ready Flask REST API for compensation analytics, designed for Azure deployment.</em></p>
<hr/>

<!-- Table of Contents -->
<h2>📖 Table of Contents</h2>
<ul>
  <li><a href="#overview">Overview</a></li>
  <li><a href="#features">Key Features</a></li>
  <li><a href="#architecture">Architecture</a></li>
  <li><a href="#getting-started">Getting Started</a>
    <ul>
      <li><a href="#prerequisites">Prerequisites</a></li>
      <li><a href="#installation">Installation</a></li>
      <li><a href="#configuration">Configuration</a></li>
    </ul>
  </li>
  <li><a href="#usage">Usage</a>
    <ul>
      <li><a href="#running-locally">Running Locally</a></li>
      <li><a href="#docker">Docker</a></li>
      <li><a href="#azure-deployment">Azure Deployment</a></li>
    </ul>
  </li>
  <li><a href="#api-reference">API Reference</a></li>
  <li><a href="#authentication">Authentication</a></li>
  <li><a href="#contributing">Contributing</a></li>
  <li><a href="#license">License</a></li>
  <li><a href="#contact">Contact</a></li>
</ul>
<hr/>

<!-- Overview -->
<h2 id="overview">🌟 Overview</h2>
<p>The <strong>Compensation API</strong> is a scalable, secure, and fully documented Flask-based service that provides compensation data insights. Designed for seamless Azure deployment, it features:</p>
<ul>
  <li>Integration with external compensation datasets</li>
  <li>Stubbed Azure AI Language &amp; Azure Machine Learning hooks</li>
  <li>Role-Based Access Control (RBAC) via JWT tokens</li>
  <li>Interactive Swagger UI (OpenAPI 3.0) documentation</li>
  <li>Container-ready with Docker and Azure Container Registry compatibility</li>
</ul>

<!-- Features -->
<h2 id="features">✨ Key Features</h2>
<ul>
  <li><strong>Data Integration</strong>: Pull and serve compensation data from industry APIs.</li>
  <li><strong>AI/ML Ready</strong>: Pre-wired Azure AI Language &amp; Machine Learning service stubs.</li>
  <li><strong>Security</strong>: JWT authentication, user roles (<code>admin</code>, <code>user</code>).</li>
  <li><strong>Documentation</strong>: Auto-generated Swagger UI at <code>/apidocs/</code>.</li>
  <li><strong>ETL Utilities</strong>: Ingest CSV or text job descriptions and process into structured data.</li>
  <li><strong>Reporting</strong>: Salary distribution charts (Matplotlib) &amp; CSV/Excel exports.</li>
  <li><strong>Dockerized</strong>: One-step Docker build &amp; run.</li>
  <li><strong>Azure Deployment</strong>: ARM templates/Bicep, App Service &amp; Key Vault integration.</li>
</ul>

<!-- Architecture -->
<h2 id="architecture">🏗️ Architecture</h2>
<p align="center">
  <img src="https://raw.githubusercontent.com/Emmcrispy/mannysAPI/main/docs/architecture.png" alt="Architecture Diagram" width="700"/>
</p>
<ul>
  <li><strong>Flask API Gateway</strong>: Routes, auth, RBAC, Swagger UI.</li>
  <li><strong>Azure SQL Database</strong>: Persistent job and user data.</li>
  <li><strong>Azure Blob Storage</strong>: File uploads (job descriptions).</li>
  <li><strong>Azure AI Language</strong>: Keyword/entity extraction (stub).</li>
  <li><strong>Azure ML Service</strong>: Semantic matching (stub).</li>
  <li><strong>Azure Key Vault</strong>: Secure secret storage.</li>
</ul>

<!-- Getting Started -->
<h2 id="getting-started">🚀 Getting Started</h2>

<h3 id="prerequisites">Prerequisites</h3>
<ul>
  <li>Python 3.8+</li>
  <li>SQL Server (local) or Azure SQL</li>
  <li>Docker (optional)</li>
  <li>Azure CLI (for deployment)</li>
  <li>Git</li>
</ul>

<h3 id="installation">Installation</h3>
<pre><code>git clone https://github.com/Emmcrispy/mannysAPI.git CompensationAPI
cd CompensationAPI
python3 -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
</code></pre>

<h3 id="configuration">Configuration</h3>
<p>Copy and edit the environment template:</p>
<pre><code>cp .env.example .env</code></pre>
<p>Then fill in:</p>
<table>
  <tr><th>Variable</th><th>Description</th></tr>
  <tr><td><code>FLASK_ENV</code></td><td><code>development</code> or <code>production</code></td></tr>
  <tr><td><code>DEV_DATABASE_URI</code></td><td>Local SQL Server connection (URL-encoded if using ODBC 18)</td></tr>
  <tr><td><code>AZURE_SQL_CONNECTION_STRING</code></td><td>Azure SQL connection string</td></tr>
  <tr><td><code>SECRET_KEY</code></td><td>JWT &amp; Flask secret</td></tr>
  <tr><td><code>BLS_API_KEY</code></td><td>External data API key</td></tr>
  <tr><td><code>AZURE_* </code></td><td>Azure service credentials</td></tr>
</table>

<!-- Usage -->
<h2 id="usage">⚙️ Usage</h2>

<h3 id="running-locally">Running Locally</h3>
<pre><code>set FLASK_APP=run.py
flask init-db admin AdminPass123
flask run --host=0.0.0.0 --port=5000
</code></pre>
<p>Browse API at <a href="http://localhost:5000/">/</a>, Swagger UI at <a href="http://localhost:5000/apidocs/">/apidocs/</a>.</p>

<h3 id="docker">Docker</h3>
<pre><code>docker build -t compensation-api .
docker run -d -p 5000:5000 --name comp-api compensation-api
</code></pre>
<p>Push to ACR and deploy to AKS or App Service as needed.</p>

<h3 id="azure-deployment">Azure Deployment</h3>
<ol>
  <li>Login with <code>az login</code>.</li>
  <li><code>az group create -n MyRG -l eastus</code></li>
  <li><code>az appservice plan create -n MyPlan -g MyRG --is-linux</code></li>
  <li><code>az webapp create -n CompensationAPIApp -g MyRG -p MyPlan --deployment-container-image-name &lt;ACR&gt;</code></li>
  <li>Configure settings in Azure Portal (Env Vars &amp; Managed Identity).</li>
</ol>

<!-- API Reference -->
<h2 id="api-reference">📡 API Reference</h2>
<table>
  <tr><th>Endpoint</th><th>Method</th><th>Description</th></tr>
  <tr><td><code>/</code></td><td>GET</td><td>Home</td></tr>
  <tr><td><code>/api/health</code></td><td>GET</td><td>Health check</td></tr>
  <tr><td><code>/api/auth/register</code></td><td>POST</td><td>User registration</td></tr>
  <tr><td><code>/api/auth/login</code></td><td>POST</td><td>Login &amp; JWT token</td></tr>
  <tr><td><code>/api/user/me</code></td><td>GET</td><td>Current user info</td></tr>
  <tr><td><code>/api/jobs/upload</code></td><td>POST</td><td>Upload job descriptions</td></tr>
  <tr><td><code>/api/jobs/search?q=</code></td><td>GET</td><td>Search jobs</td></tr>
  <tr><td><code>/api/jobs/match</code></td><td>POST</td><td>Match jobs</td></tr>
  <tr><td><code>/api/bls/data</code></td><td>GET</td><td>Fetch compensation data</td></tr>
  <tr><td><code>/api/reports/salary_distribution</code></td><td>GET</td><td>Salary chart (PNG)</td></tr>
  <tr><td><code>/api/reports/export/matches</code></td><td>POST</td><td>Export matches CSV</td></tr>
</table>

<!-- Authentication -->
<h2 id="authentication">🔐 Authentication</h2>
<p>Use the <code>/api/auth/login</code> endpoint to obtain a Bearer token:</p>
<pre><code>curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"AdminPass123"}'
</code></pre>
<p>Then include in your requests:</p>
<pre><code>curl http://localhost:5000/api/user/me \
  -H "Authorization: Bearer &lt;ACCESS_TOKEN&gt;"
</code></pre>

<!-- Contributing -->
<h2 id="contributing">🤝 Contributing</h2>
<p>Contributions, issues, and feature requests are welcome! Please fork the repo and submit a pull request. See <code>CONTRIBUTING.md</code> for details.</p>

<!-- License -->
<h2 id="license">📄 License</h2>
<p>This project is licensed under the <a href="LICENSE">MIT License</a>.</p>

<!-- Contact -->
<h2 id="contact">📬 Contact</h2>
<p>Created by <strong>Emmanuel Crispin</strong> &mdash;</p>
