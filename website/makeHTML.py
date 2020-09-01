#!/usr/bin/env python
"""
Generating html

purpose: create an html page

for example:

filename = 'web_page_test_0.html'

## Creating the first section
header = sections('html',title='HTML page')
header.add_to_section('<h2> Example Page </h2>')
header.add_figure(["./img/sky_plot.png"],caption=['Distributions of the sources on the sky'])

## Creating the second section
second = sections('Second',title='Second Section')
second.add_to_section(<p> my text </p>)
second.add_slide_images(['first_picture.png','first_picture.png'])

build_index_page([header,second],fname=filename)
"""

def build_index_page(section_list,fname,header=None):
	## closing sections
	for si in section_list: si.close_section()

	## joining sections content
	contents = '\n'.join([si.section_syntax for si in section_list])

	## creating navigation bar
	nav_bar_content = '\n'.join([si.line_navbar() for si in section_list])
	nav_bar = NAVBAR%dict(sections=nav_bar_content)

	## setiing header
	if header is None: header = """\n"""

	## putting content and navigation bar on the index synthax
	index = INDEX%dict(navigation_bar=nav_bar, content=contents, header=header)

	with open(fname,'w') as out:
		out.write(index)

	print('Validation page created with sucsess!')
	print('--> %s'%(fname))


from itertools import count
class sections:
	"""This class manages the creation of the webpage sections"""
	_ks = count(0)
	_ks2 = count(0)

	def __init__(self,name,title=None,files=None):
		self.id = name.lower()
		self.name = name
		
		self.k = next(self._ks)

		if title is not None: self.title = '%i -'%(self.k) + title
		else: self.title = '%i -'%(self.k) + name

		self.section_syntax = self.make_section_header()
		
	def make_section_header(self):
		return SECTION%dict(id=self.id,title=self.title)

	def add_to_section(self,string):
		self.section_syntax += '\n'+string
		return self.section_syntax

	def close_section(self):
		self.section_syntax += '\n  </div>\n</div>'

	def line_navbar(self):
		LINE = """  <a href="#%(id)s" class="w3-bar-item w3-btn w3-text-white">%(name)s</a>"""
		return LINE%dict(id=self.id,name=self.name)

	def add_figure(self,files,caption=None):
		if caption is None:
			caption = ['Figure %i.%i '%(self.k,i) for i,img in enumerate(files)]
		else:
			caption = ['Figure %i.%i :'%(self.k,i)+ci for i,ci in enumerate(caption)]
		
		bulk = '\n'.join([FIGURE%dict(fname=img, caption =ci) for img,ci in zip(files,caption) ])

		return self.add_to_section(bulk)

	def add_slide_images(self,files):
		ks = next(self._ks2)
		block = '\n'.join([LINE1%dict(img=img, k=ks) for img in files])
		block2 = '\n'.join([LINE2%dict(count=i+1, k=ks) for i in range(len(files))])
		img_slide_synthax = IMAGE_GRID % dict(block=block, block2=block2, k=ks)

		return self.add_to_section(img_slide_synthax)
	
	def add_html_table(self,dicto,title='',buttom=None):
		header = """<br> <h4> Table %(title)s </h4>
		<table class="w3-table-all w3-hoverable">"""%dict(title=title)
		
		if buttom is not None:
			ks = next(self._ks2)
			ac = ACCORDION%dict(k=ks,label=buttom)
			header = ac+header

		table_lines = ''.join( [TABLE%dict(key=key,val=dicto[key]) for key in dicto] )
		table_synthax = header +'\n'+table_lines + '\n</table> </br>'
		
		if buttom:
			table_synthax += '\n</div>'

		return self.add_to_section(table_synthax)

	def row_cluster_info(self,table,buttom=None):
		header = """<table class="w3-table-all w3-hoverable">"""
		
		if buttom is not None:
			ks = next(self._ks2)
			ac = ACCORDION%dict(k=ks,label=buttom)
			header = ac+header
		
		header_table = """\n  <thead>\n    <tr class="w3-light-grey">"""+cluster_info

		bulk = cluster_info_row.format(table['CID'],table['RA'],table['DEC'],table['redshift'])
		table_synthax = header+header_table+bulk

		return self.add_to_section(table_synthax)

	def close_page(self):
		self._ks = 0
		self._ks2 = 0

cluster_info = """
  <thead>
    <tr class="w3-light-grey">
	  <th>CID</th>
      <th>RA</th>
      <th>DEC</th>
      <th>redshift</th>
    </tr>
  </thead>
"""
cluster_info_row="""
  <tbody>
    <tr>
      <th>{}</th>
      <td>{:.5f}</td>
      <td>{:5f}</td>
      <td>{:.3f}</td>
    </tr>
  </tbody>
</table>	
"""
columns_type = ['i','.5f','.5f','.3f','.1f']

ACCORDION = """
<button onclick="myFunction('Demo%(k)s')" class="w3-btn w3-block w3-black w3-left-align" style="width:50%%"><b>%(label)s</b> </button>
<div id="Demo%(k)s" class="w3-container w3-hide">
"""

TABLE = """
  <tr>
      <td>%(key)s</td>
      <td>%(val)s</td>
  </tr>
"""

INDEX = """
<!DOCTYPE html>
<html>
<title>astro-visualization: Validation Page</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<style>
body, h1,h2,h3,h4,h5,h6 {font-family: "Montserrat", sans-serif}
.w3-row-padding img {margin-bottom: 16px}
/* Set the width of the sidebar to 120px */
.w3-sidebar {width: 32px;background: #222;}
/* Add a left margin to the "page content" that matches the width of the sidebar (120px) */
/* Remove margins from "page content" on small screens */
@media only screen and (max-width: 600px) {#main {margin-left: 0}}
</style>
<body class="w3-white">

<header class="w3-container w3-top w3-black w3-xlarge">
  <span class="w3-right w3-padding">astro-visualization</span>
</header>

%(navigation_bar)s


<!-- PAGE CONTENT -->
<div class="w3-main w3-content" style="max-width:1600px;margin-top:60px">
<div class="w3-padding-large" style="max-width:1600px;margin-top:60px" id="main">

%(header)s

%(content)s

  <!-- Footer -->
  <footer class="w3-content w3-padding-64 w3-text-grey w3-xlarge">
    <a href="https://github.com/estevesjh/ccopa"> <i class="fa fa-github w3-hover-opacity"></i> </a>
    <p class="w3-medium">Fermi wiki page <a href="https://www.w3schools.com/w3css/default.asp" target="_blank" class="w3-hover-text-green">w3.css</a></p>
  <!-- End footer -->
  </footer>
</div>
<!-- END PAGE CONTENT -->
</div>

</body>
</html>
"""

SECTION = """
<div class="w3-content w3-justify w3-text-grey w3-padding-64" id="%(id)s">
  <h2 class="w3-padding-16 w3-text-grey">%(title)s</h2>
  <div class="w3-section">
"""

NAVBAR = """
<!-- Overlay effect when opening sidebar on small screens -->
<div class="w3-overlay w3-animate-opacity" onclick="w3_close()" style="cursor:pointer" title="close side menu" id="myOverlay"></div>

<!-- Navbar on small screens (Hidden on medium and large screens) -->
<div class="w3-top">
<div class="w3-bar w3-theme w3-top w3-left-align w3-large">
<!--div class="w3-bar w3-theme w3-top w3-left-align w3-large"-->
%(sections)s
</div>
</div>
"""

FIGURE = """
  <figure>
	<td> <a id="%(fname)s"></a> <img src="%(fname)s" style="width:100%%"> </td>
	<figurecaption> <h4> %(caption)s </h4> </figurecaption>
  </figure>
"""

LINE1 ="""  <img class="mySlides%(k)s" src="%(img)s" style="width:100%%">"""
LINE2 ="""  <button class="w3-button demo%(k)s" onclick="currentDiv%(k)s(%(count)s)">%(count)s</button>"""

IMAGE_GRID = """
<div class="w3-content" style="max-width:800px">
%(block)s
</div>

<br>
<div class="w3-center">
Figure
%(block2)s
</div>

<script>
var slideIndex = 1;
showDivs%(k)s(slideIndex);

function currentDiv%(k)s(n) {
  showDivs%(k)s(slideIndex = n);
}

function showDivs%(k)s(n) {
  var i;
  var x = document.getElementsByClassName("mySlides%(k)s");
  var dots = document.getElementsByClassName("demo%(k)s");
  if (n > x.length) {slideIndex = 1}    
  if (n < 1) {slideIndex = x.length}
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";  
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" w3-black", "");
  }
  x[slideIndex-1].style.display = "block";  
  dots[slideIndex-1].className += " w3-black";
}
</script>
"""
__author__ = "Johnny Esteves"
