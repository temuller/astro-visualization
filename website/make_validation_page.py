#!/usr/bin/env python
"""
Generating astro-visualization web page
"""
__author__ = "Johnny Esteves"


HEADER = """
	<header class="w3-container w3-padding-32 w3-center w3-black" id="home">
	<h1 class="w3-jumbo"> Astro-Visualization </h1>
		<h4> A repository for pretty astronomical plots </h4>
	</header>

	<div class="w3-content w3-justify w3-text-grey w3-padding-64">
	<h3> Welcome to Astro-Visualization! In this website you can find several examples of pretty astronomical plots, and best of all, their source code! If you see a plot you like, just copy the source code and modify it to your convenience. Want to contribute with a pretty plot of your own? Get in touch with us! </h3>

	<p> This website is hosted in a <a href="https://github.com/temuller/astro-visualization"> Github repository</a>. </p>
	</div>
"""

DESCRIPTION = """
	<p>
	</p>
"""

CONTRIBUTING = """
	<p> Do you have a pretty plot you would like to share with the rest of the astronomy community? Wonderful! We require the following: </p>

	<ul>
  	<li>Your name (ideally as it appears on your publications). Affiliation is optional.</li>
  	<li>An image of your plot (use the most common formats (e.g., png, jpg, pdf, etc).</li>
  	<li>The link to the original plot, if any (e.g., publication, website, etc.)</li>
	<li>The caption of the plot.</li>
	<li>The source code. We don't require the data, but try to re-write the code to be as generic as possible so others can easilly understand how it works. Don't forget to include comments as a guide.</li>
	<li>Create a `metada.txt` file with points 1 and 3. Compress all the files (metadata, image and source code) in a single file (zip, tar, etc.).</li>
	<li>Send it to <a href="https://github.com/temuller/astro-visualization/tree/test_branch#contributors">us</a>!</li>
	</ul>

	<p> You can find an example in our <a href="https://github.com/temuller/astro-visualization/tree/master">Github repository</a>.</p>
"""

test_code = """var message = "hello world!";
alert(message);
"""
import glob

def get_image_path():
	# resul_fname_list = ['./img/mu_identity_4.png','./img/mu_residual_4_ntrue.png']
	fname_list0 = glob.glob("../img/stars_*")
	fname_list0.reverse()

	fname_list1 = glob.glob("../img/galaxies_*.png")
	fname_list1.reverse()

	fname_list2 = glob.glob("./img/slide_*")

	return [fname_list0,fname_list1,fname_list2]

def main():
	from makeHTML import sections, build_index_page

	filename = 'index.html'
	f1, f2, f3 = get_image_path()

	## Creating the first section
	header = sections('astro',title='Astro Visualization')
	header.add_to_section(DESCRIPTION)
	header.add_to_section('<h4> First Example </h4>')

	header.add_figure(["./img/example.png"],caption=['color magnitude relaiton for galaxies on DES Y1'])
	header.add_to_section('<p> The syntax for this plot is given by:')
	header.add_code_block('',infile='./img/example.py')

	## Creating the gallery section
	gal = sections('gallery',title='Gallery')
	gal.add_grid_figure('./img/slide_01.png','Example A','bla',begin=True)
	gal.add_grid_figure('./img/slide_02.png','Example B','bla')
	gal.add_grid_figure('./img/slide_03.png','Example C','bla')
	#gal.add_grid_figure('./img/slide_03.png','Example D','bla',class_type='type3')
	gal.add_grid_figure('./img/example.png','Example D','bla',class_type='Galaxy',close=True)

	# gal.add_to_section('Take a look in our examples')
	# gal.add_slide_images(f3)

	## Creating the Third section
	cont = sections('contributing',title='Contributing')
	cont.add_to_section(CONTRIBUTING)

	build_index_page([gal,header, cont],filename,header=HEADER)

main()
