# pymesoamerica

Python library to interact with the [Loubat codices in the FAMSI database](http://www.famsi.org/research/loubat/). Mainly concerned with providing a simple method of retrieving images in bulk to aid analysis (either machine or human).

## Usage

### Installation

```bash
pip install pymesoamerica
``` 

### Commands

 - `pymesoamerica codices` - Lists available codices for download.
   - Currently available:
     - borbonicus
     - borgia
     - cospi
     - fejéváry-mayer
     - magliabecchiano
     - telleriano-remensis
     - tonalamatl-aubin
     - vaticanus-3738-a
     - vaticanus-3773-b

 - `pymesoamerica download [codex]` - Downloads a specific codex for local analysis.

 - `pymesoamerica download-all` - Downloads all available codices for local analysis.

 - `pymesoamerica images` - Provides a hierarchial list of URLS pointing to individual codex pages grouped by codices.