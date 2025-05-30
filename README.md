# Noirscan v1.0

<p align="center">
  <a href="https://www.python.org/">
    <img alt="Python" src="https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white&style=for-the-badge">
  </a>
  <a href="https://www.torproject.org/">
    <img alt="TOR Supported" src="https://img.shields.io/badge/TOR-Supported-7D4698?logo=tor&logoColor=white&style=for-the-badge">
  </a>
</p>

**Noirscan** is an extensible, ethical, and robust Python crawler designed to explore both the surface web and the dark web (via TOR). It is built for research, analysis, and data extraction in formats suitable for AI training, cybersecurity, and law enforcement use-cases. Noirscan puts emphasis on modularity, ethical compliance, and high data quality.

Noirscan is still in alpha stage and more functionality will be added.

---

## 🚀 Features

- **TOR & Surface Web Support:** Crawl standard and .onion sites using SOCKS5H over TOR.
- **Depth-Limited Recursive Crawling:** Configurable crawl depth to control scope and resource use.
- **User-Agent Randomization/Override:** Mimic different browsers or set your own.
- **Ethical Crawling:** robots.txt parsing (with CLI bypass option) and clear warnings to users.
- **Structured Data Extraction:** Extracts page titles, cleaned main text, links, and more.
- **Automatic Metadata Collection:** Timestamps, IP, geolocation, and more.
- **Rich Output:** Saves results as structured, well-documented JSON for easy downstream analysis or ingestion.
- **Colorized, User-Friendly CLI:** Clear prompts, helpful summaries, and progress info.
- **Modular Codebase:** Easily extend scraping logic, add new extractors, or integrate with external systems.

---

## ⚡ Quickstart

### **Requirements**
- Python 3.9+
- TOR running locally (default port 9050)
- All dependencies in `requirements.txt`

### **Installation**
```bash
git clone https://github.com/TencoDev/Noirscan.git
cd Noirscan
pip install -r requirements.txt
```

### **Usage Example**
```bash
# Basic crawl (surface web or dark web)
python noirscan/main.py --url "http://example.com" --depth 1

# With custom user agent and robots.txt enabled
python noirscan/main.py --url "http://somesite.com" --user-agent "MyBot/1.0" --ignore-robots False

# Crawl a .onion site with output saved to JSON
python noirscan/main.py --url "http://somedarkweb.onion" --save --depth 2
```

---

## 🛡️ Ethical & Legal Notice

> ⚠️ **Important:** Noirscan is a research tool. You are responsible for all use.  
> - Always respect local laws and the terms of service of target sites.  
> - By default, Noirscan respects robots.txt and provides clear CLI warnings.
> - For law enforcement or sensitive use, always consult legal counsel before deploying.

---

## 🧩 Project Structure

```
noirscan/
  ├── main.py         # CLI entrypoint
  ├── crawler.py      # Crawler logic (class-based, extensible)
  ├── utils.py        # Utility functions (cleaning, printing, saving)
  ├── network.py      # Network helpers (TOR, IP, geolocation)
  ├── models.py       # ScrapedPage and data models
  ├── config.py       # User agents, timeouts, config
  └── output/         # (auto-created) JSON output files
requirements.txt
README.md
```

---

## 🛠️ Extending Noirscan

- **Custom Extraction:** Add new parsing methods in `models.py` or utility functions in `utils.py`.
- **Plugins:** Integrate entity recognizers, ML/NLP pipelines, or custom exporters.
- **CLI:** Easily extendable, just add new flags and wire to the `Crawler` class.

---

## 📅 Future Plans

- **Advanced Content Extraction:** Use NLP/ML for better main text, keyword, language, and entity extraction.
- **Session Management:** Support for cookies, login, and authenticated crawling.
- **Distributed Crawling:** Multi-process or multi-machine support for large-scale scans.
- **Database Export:** Native support for MongoDB, Elastic, or SQL.
- **UI Dashboard:** Live crawl progress and data visualization.
- **Unit & Integration Tests:** Expand testing for reliability and CI/CD.
- **Crawler Politeness:** Configurable delays, concurrency, and auto-throttling.
- **Multi-format Output:** CSV, Parquet, and direct data-lake integration.
- **Dark Web Intelligence:** Plugins for dark web threat hunting, marketplace detection, etc.

---

## 👤 Author

- [TencoDev](https://github.com/TencoDev)

---

## 🙌 Contributing

Pull requests and suggestions are welcome!  
Please open an issue to discuss any major changes first.

---

## 📜 License

MIT License
