<h1 align="center">🚀 Job-Matching API</h1>
<p align="center">A modular Flask REST API for uploading, processing, and matching job descriptions against compensation data.</p>
<hr />

<h2>🔍 Features</h2>
<ul>
  <li>Microsoft SQL Server (local) &amp; Azure SQL (prod)</li>
  <li>JWT-based authentication &amp; role-based access control (RBAC)</li>
  <li>Azure service stubs: Blob Storage, Key Vault, AI Language, ML</li>
  <li>Interactive Swagger/OpenAPI 3.0 documentation</li>
  <li>Job upload (text &amp; CSV), ETL utilities</li>
  <li>Rule-based &amp; ML-enhanced matching engine</li>
  <li>BLS.gov API integration</li>
  <li>Salary visualization (Matplotlib)</li>
  <li>CSV/Excel export endpoints</li>
</ul>

<h2>📋 Requirements</h2>
<table>
  <thead>
    <tr><th>Variable</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td><code>FLASK_ENV</code></td><td><code>development</code> or <code>production</code></td></tr>
    <tr><td><code>DEV_DATABASE_URI</code></td><td>Local SQL Server URI<br><small>(use <code>odbc_connect</code> with Driver 18 flags)</small></td></tr>
    <tr><td><code>AZURE_SQL_CONNECTION_STRING</code></td><td>Azure SQL DB URI</td></tr>
    <tr><td><code>SECRET_KEY</code></td><td>JWT signing secret</td></tr>
    <tr><td><code>BLS_API_KEY</code></td><td>BLS.gov API key</td></tr>
    <tr><td><code>AZURE_STORAGE_ACCOUNT_NAME</code></td><td>Blob Storage account</td></tr>
    <tr><td><code>AZURE_TEXT_ANALYTICS_KEY</code></td><td>AI Language key</td></tr>
    <tr><td><code>AZURE_TEXT_ANALYTICS_ENDPOINT</code></td><td>AI Language endpoint</td></tr>
    <tr><td><code>AZURE_KEY_VAULT_NAME</code></td><td>Key Vault name</td></tr>
  </tbody>
</table>

<h2>⚙️ Local Setup</h2>
<pre><code># 1. Clone &amp; enter directory
git clone https://github.com/your-org/job-matching-api.git
cd job-matching-api

# 2. Create &amp; activate venv
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy &amp; fill .env
cp .env.example .env
# Edit .env with your values

# 5. Initialize DB &amp; seed
set FLASK_APP=run.py
flask init-db admin AdminPass123

# 6. Run the server
flask run
# or
python run.py
</code></pre>

<h2>🔗 API Endpoints</h2>
<ul>
  <li><strong>Swagger UI</strong>: <a href="http://localhost:5000/apidocs/">/apidocs/</a></li>
  <li><strong>Home</strong>: <code>GET /</code></li>
  <li><strong>Health</strong>: <code>GET /api/health</code></li>
  <li><strong>Register</strong>: <code>POST /api/auth/register</code></li>
  <li><strong>Login</strong>: <code>POST /api/auth/login</code></li>
  <li><strong>User Info</strong>: <code>GET /api/user/me</code> (Bearer token)</li>
  <li><strong>Upload Jobs</strong>: <code>POST /api/jobs/upload</code> (file + auth)</li>
  <li><strong>Search Jobs</strong>: <code>GET /api/jobs/search?q=engineer</code></li>
  <li><strong>Match Jobs</strong>: <code>POST /api/jobs/match</code></li>
  <li><strong>BLS Data</strong>: <code>GET /api/bls/data?seriesid=...&amp;startyear=...&amp;endyear=...</code></li>
  <li><strong>Salary Chart</strong>: <code>GET /api/reports/salary_distribution</code></li>
  <li><strong>Export Matches</strong>: <code>POST /api/reports/export/matches</code></li>
</ul>

<h2>🐳 Docker</h2>
<pre><code># Build &amp; start containers
docker-compose build
docker-compose up -d

# Init DB inside container
docker-compose exec web bash
flask init-db admin AdminPass123
exit

# API &amp; Swagger at http://localhost:5000
</code></pre>

<h2>🔧 Git Workflow</h2>
<ul>
  <li><strong>main</strong>: production-ready (protected)</li>
  <li><strong>develop</strong>: integration branch</li>
  <li>Feature branches: <code>feature/xyz</code></li>
  <li>Release branches: <code>release/vX.Y</code></li>
  <li>Hotfix branches: <code>hotfix/issue-123</code></li>
  <li>Commit messages: imperatives, reference issue IDs</li>
</ul>

<hr />
<p align="center">© 2025 Your Company • <a href="LICENSE">MIT License</a></p>
