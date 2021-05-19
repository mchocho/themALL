<div align="center">
   <h1>themALL🛍️</h1>
   <h4>Compare prices from dozens of well known e-commerce and b&m retailers.</h4>
   [![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)&nbsp;&nbsp;
   [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
</div>

## `Install`

```bash
git clone https://github.com/mchocho/themALL

pip install -r requirements.txt

#Search for a harddrive disk
py themall "1 tb hdd"

#Save your search results in a txt file
py themall "resident evil village" > results.txt
```

<p>For more resources you'll have to download the <a href="https://github.com/mozilla/geckodriver/releases">Firefox web driver</a> and point to it in a .env file. After downloading the web driver run:</p>

```bash
vi .env
```

<p>Replace the value "Path/to/geckodriver" with the path to web driver. Save the .env file and exit vim. Then run: </a>

```bash
py -m unittest test/test_themall.py
```
## `Available stores`

<table>
	<tr>
		<th>Name</th>
		<th>Country</th>
		<th>Requires web driver</th>
	</tr>
	<tr>
		<td><a href="https://www.bidorbuy.co.za/">Bidorbuy</a></td>
		<td>&#127487;&#127462;</td>
		<td>No</td>
	</tr>
	<tr>
		<td><a href="https://www.builders.co.za/">Builders</a></td>
		<td>&#127487;&#127462;</td>
		<td>No</td>
	</tr>
	<tr>
		<td><a href="https://www.cashcrusaders.co.za/">Cash Crusaders</a></td>
		<td>&#127487;&#127462;</td>
		<td>No</td>
	</tr>
	<tr>
		<td><a href="https://www.evetech.co.za/">EVETECH</a></td>
		<td>&#127487;&#127462;</td>
		<td>No</td>
	</tr>
	<tr>
		<td><a href="https://www.game.co.za/">Game</a></td>
		<td>&#127487;&#127462;</td>
		<td>No</td>
	</tr>
	<tr>
		<td><a href="https://www.hificorp.co.za/">HiFi Corp</a></td>
		<td>&#127487;&#127462;</td>
		<td>No</td>
	</tr>
	<tr>
		<td><a href="https://www.incredible.co.za/">Incredible</a></td>
		<td>&#127487;&#127462;</td>
		<td>No</td>
	</tr>
	<tr>
		<td><a href="https://www.loot.co.za/">Loot.co.za</a></td>
		<td>&#127487;&#127462;</td>
		<td>No</td>
	</tr>
	<tr>
		<td><a href="https://www.makro.co.za/">Makro</a></td>
		<td>&#127487;&#127462;</td>
		<td>No</td>
	</tr>
	<tr>
		<td><a href="https://www.pnp.co.za/">Pick n Pay</a></td>
		<td>&#127487;&#127462;</td>
		<td>No</td>
	</tr>
	<tr>
		<td><a href="https://www.raru.co.za/">Raru</a></td>
		<td>&#127487;&#127462;</td>
		<td>No</td>
	</tr>
	<tr>
		<td><a href="https://www.takealot.com/">Takealot.com</a></td>
		<td>&#127487;&#127462;</td>
		<td>Yes</td>
	</tr>
	<tr>
		<td><a href="https://www.thekidzone.co.za/">The Kid Zone</a></td>
		<td>&#127487;&#127462;</td>
		<td>No</td>
	</tr>
	<tr>
		<td><a href="https://www.wantitall.co.za">WantItAll.co.za</a></td>
		<td>&#127487;&#127462;</td>
		<td>No</td>
	</tr>
</table>

## `Quick tips`

* Precise searches yield the best results.
* If the table columns are too wide, just zoom out, retry the search, then zoom back in once it produces output.
* Please share this with your friends.
