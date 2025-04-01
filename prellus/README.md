# Prellus Portal

Quick setup for MacOS users:

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop)

2. Configure Docker Desktop:
   - Open Docker Desktop
   - Click Settings (⚙️) > Resources
   - Set Memory to at least 12GB
   - Click 'Apply & Restart'

3. Open Terminal and run:
   ```bash
   cd prellus
   make up
   ```
   The portal will open automatically in your browser.

4. When done:
   ```bash
   make down
   ```

Commands:
- `make logs` - View activity logs
- `make monitor` - Check system status

System Requirements:
- Minimum 12GB RAM allocated to Docker
- Recommended: 16GB+ total system RAM
- Docker Desktop with sufficient resources

Support: 
- If portal doesn't open, visit http://localhost:3000
- If you see memory errors, check Docker Desktop memory allocation 