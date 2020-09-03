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

		if title is not None: self.title = title
		else: self.title = name

		self.section_syntax = self.make_section_header()
		
	def make_section_header(self):
		return SECTION%dict(id=self.id,title=self.title)

	def add_to_section(self,string):
		self.section_syntax += '\n'+string
		return self.section_syntax

	def close(self,syntax):
		return syntax+CLOSE_GRID_GALLERY

	def close_section(self):
		self.section_syntax += '\n  </div>\n</div>'

	def line_navbar(self):
		LINE = """  <a href="#%(id)s" class="w3-bar-item w3-btn w3-text-white">%(name)s</a>"""
		return LINE%dict(id=self.id,name=self.name)

	def add_figure(self,files,caption=None):
		if caption is None:
			caption = ['Figure %i '%(i+1) for i,img in enumerate(files)]
		else:
			caption = ['Figure %i :'%(i+1)+ci for i,ci in enumerate(caption)]
		
		bulk = '\n'.join([FIGURE%dict(fname=img, caption =ci) for img,ci in zip(files,caption) ])

		return self.add_to_section(bulk)

	def add_slide_images(self,files):
		ks = next(self._ks2)
		block = '\n'.join([LINE1%dict(img=img, k=ks) for img in files])
		block2 = '\n'.join([LINE2%dict(count=i+1, k=ks) for i in range(len(files))])
		img_slide_synthax = IMAGE_GRID % dict(block=block, block2=block2, k=ks)

		return self.add_to_section(img_slide_synthax)

	def add_grid_figure(self,fname,title,caption,class_type='type1',begin=False,close=False):
		if begin:
			self.add_to_section(GRIDGALLERY)
		
		line = IMG_GRID_GALLERY%dict(image=fname,caption=caption,key=title,class_type=class_type)
		if close: line = self.close(line)
		return self.add_to_section(line)

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

	def add_code_block(self,text,infile=None):
		if infile is None:
			code_block_line = CODE_BOX%dict(syntax=text)
		else:
			myfile = open(infile,'r')
			code_block_line = CODE_BOX%dict(syntax=myfile.read())
		
		return self.add_to_section(code_block_line)

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
<link rel="stylesheet" href="http://codemirror.net/lib/codemirror.css">
<script src="http://codemirror.net/lib/codemirror.js"></script>
<script src="http://codemirror.net/mode/python/python.js"></script>
<style>

body, h1,h2,h3,h4,h5,h6 {font-family: "Montserrat", sans-serif}
.w3-row-padding img {margin-bottom: 16px}
/* Set the width of the sidebar to 120px */
.w3-sidebar {width: 32px;background: #222;}
/* Add a left margin to the "page content" that matches the width of the sidebar (120px) */
/* Remove margins from "page content" on small screens */
@media only screen and (max-width: 600px) {#main {margin-left: 0}}

#gallery-2 {
  width: 100%%;
  background: #151515;
  -webkit-user-select: none;
  -moz-user-select: none;  
  user-select: none;
}

* {
  box-sizing: border-box;
}

body {
  background-color: #f1f1f1;
  padding: 20px;
  font-family: Arial;
}

/* Center website */
.main {
  max-width: 1000px;
  margin: auto;
}

h1 {
  font-size: 50px;
  word-break: break-all;
}

.row {
  margin: 10px -16px;
}

/* Add padding BETWEEN each column */
.row,
.row > .column {
  padding: 8px;
}

/* Create three equal columns that floats next to each other */
.column {
  float: left;
  width: 33.33%%;
  display: none; /* Hide all elements by default */
}

/* Clear floats after rows */ 
.row:after {
  content: "";
  display: table;
  clear: both;
}

/* Content */
.content {
  background-color: light-grey;
  padding: 10px;
}

/* The "show" class is added to the filtered elements */
.show {
  display: block;
}

/* Style the buttons */
.btn {
  border: none;
  outline: none;
  padding: 12px 16px;
  background-color: white;
  cursor: pointer;
}

.btn:hover {
  background-color: #ddd;
}

.btn.active {
  background-color: #666;
  color: white;
}
.btn {
  background-color: #ddd;
  border: none;
  color: black;
  padding: 16px 32px;
  text-align: center;
  font-size: 16px;
  margin: 6px 4px;
  transition: 0.3s;
}

.btn:hover {
  background-color: #3e8e41;
  color: white;
}

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

CODE_BOX = """
  <div class="w3-border">
    <div class="w3-container w3-margin w3-light-grey">
      <pre><code id="cython_code">%(syntax)s
    </div>
  </div>
<script type="text/javascript">
  window.onload = function(){
      var codeElement = document.getElementById('cython_code');
      var code = codeElement.innerText;
    
      codeElement.innerHTML = "";
    
      var codeMirror = CodeMirror(
        codeElement,
        {
          value: code,
          mode: "python",
          theme: "default",
          lineNumbers: true,
          readOnly: true
        }
      );
  };
</script>
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

GRIDGALLERY = """<div id="myBtnContainer">
  <button class="btn active" onclick="filterSelection('all')"> Show all</button>
  <button class="btn" onclick="filterSelection('type1')"> Type 1</button>
  <button class="btn" onclick="filterSelection('type2')"> Type 2</button>
  <button class="btn" onclick="filterSelection('type3')"> Type 3</button>
</div>
<!-- Portfolio Gallery Grid -->
<div class="row">
"""

IMG_GRID_GALLERY="""<div class="column %(class_type)s">
    <div class="content">
    <div class="w3-ul w3-border w3-hover-shadow w3-light-grey">
      <img src="%(image)s" alt="%(key)s" style="width:100%%">
      <h4>%(key)s</h4>
      <p>%(caption)s</p>
    </div>
    </div>
</div>
"""

CLOSE_GRID_GALLERY="""</div>
<script>
filterSelection("all")
function filterSelection(c) {
  var x, i;
  x = document.getElementsByClassName("column");
  if (c == "all") c = "";
  for (i = 0; i < x.length; i++) {
    w3RemoveClass(x[i], "show");
    if (x[i].className.indexOf(c) > -1) w3AddClass(x[i], "show");
  }
}

function w3AddClass(element, name) {
  var i, arr1, arr2;
  arr1 = element.className.split(" ");
  arr2 = name.split(" ");
  for (i = 0; i < arr2.length; i++) {
    if (arr1.indexOf(arr2[i]) == -1) {element.className += " " + arr2[i];}
  }
}

function w3RemoveClass(element, name) {
  var i, arr1, arr2;
  arr1 = element.className.split(" ");
  arr2 = name.split(" ");
  for (i = 0; i < arr2.length; i++) {
    while (arr1.indexOf(arr2[i]) > -1) {
      arr1.splice(arr1.indexOf(arr2[i]), 1);     
    }
  }
  element.className = arr1.join(" ");
}


// Add active class to the current button (highlight it)
var btnContainer = document.getElementById("myBtnContainer");
var btns = btnContainer.getElementsByClassName("btn");
for (var i = 0; i < btns.length; i++) {
  btns[i].addEventListener("click", function(){
    var current = document.getElementsByClassName("active");
    current[0].className = current[0].className.replace(" active", "");
    this.className += " active";
  });
}
</script>
"""

CLOSE_SLIDER="""</div>
<script>
jQuery(document).ready(function() {
  $('#gallery-2').royalSlider({
    fullscreen: {
      enabled: true,
      nativeFS: true
    },
    controlNavigation: 'thumbnails',
    thumbs: {
      orientation: 'vertical',
      paddingBottom: 4,
      appendSpan: true
    },
    transitionType:'fade',
    autoScaleSlider: true, 
    autoScaleSliderWidth: 960,     
    autoScaleSliderHeight: 600,
    loop: true,
    arrowsNav: false,
    keyboardNavEnabled: true

  });
});
</script>
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
