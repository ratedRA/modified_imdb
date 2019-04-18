from django.shortcuts import render
from .models import Movies, Star_cast, Director
from bs4 import BeautifulSoup
import requests
import re
import csv
from collections import defaultdict

def home_page(request):
	context = {
		'result' : 'via home_page'
	}
	return render(request, 'home.html', context)

def put_into_db(request):

	url = 'https://www.imdb.com/india/top-rated-indian-movies/'
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'lxml')

	movies = soup.select('td.titleColumn')
	links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]
	cast = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
	ratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]
	Movies.objects.all().delete()

	for index in range(0, len(movies)):
		if(index == 200):
			break
		movie_string = movies[index].get_text()
		add_url ='https://www.imdb.com'+ links[index]
		a = requests.get(add_url).text
		b = BeautifulSoup(a, 'lxml')
		crew =''
		table = b.find('table', class_='cast_list')

		rows=list()
		for tr in table.find_all("tr"):
			rows.append(tr)
		for el in rows:
			for td in el.find_all('td', class_ = '' ):
				if len(crew) > 0:
					crew+= ',' + td.text
				else:
					crew+= td.text
		
		l = cast[index].split(',')
		director = l[0]
		starCast = ''
		for actors in range(1, len(l)):
			if actors == 1:
				starCast += l[actors]
			else:
				starCast += ','+l[actors]
		language = ''
		lang = b.find_all('div', class_ = 'article')
		for r in lang:
			for ele in r.find_all('div', class_ = 'txt-block'):
				try:
					x = ele.find('h4', class_='inline').text
					if x == 'Language:':
						language += ele.find('a').text
				except:
					pass
		crew = crew.replace('\n','')
		movie = (' '.join(movie_string.split()).replace('.', ''))
		movie_title = movie[len(str(index))+1:-7]
		year = re.search("\((.*?)\)", movie_string).group(1)

		
		CastModel = Star_cast()
		CastModel.cast_name = starCast
		CastModel.save()

		directorModel = Director()
		directorModel.director = director
		directorModel.save()

		mymodel = Movies()
		mymodel.title = movie_title
		mymodel.year = year
		mymodel.cast = CastModel
		mymodel.director = directorModel
		mymodel.rating = ratings[index][0:3]
		mymodel.crew = crew
		mymodel.language = language
		mymodel.save()


	context = {
		'result' : 'done !'
	}
	return render(request, 'home.html', context)

def top_20_actors(request):

	qs = Movies.objects.all().order_by('-rating')[:20]
	res = []
	for i in qs:
		data = {'actor' : i.cast.cast_name}
		res.append(data)


	context = {
		'actors_from_db' : res
	}

	return render(request, 'actors_list.html', context)


def unique_actors(request):

	actors_count = defaultdict(lambda : 0)
	actors_from_db = Movies.objects.values('crew')

	for actors in actors_from_db:
		res = actors['crew'].split(',')
		for elements in res:
			x = elements
			actors_count[x] += 1

	actors_count = sorted(actors_count.items(), key = lambda x:x[1])
	result = ''
	imdb = []
	#print(actors_count)
	for items in actors_count:
		if items[1] > 1:      # for reducing the time complexity
			break
		else:
			if items[1] == 1:
				if len(result) == 0:
					result += items[0]
				else:
					result += ',' + items[0]
				data = {'name':items[0]}
				imdb.append(data)
	context = {
		'unique_actors' : imdb
	}

	return render(request, 'unique_actors.html', context)

def top_20_act_dir(request):

	qs = Movies.objects.all().order_by('-rating')[:20]
	res = []
	for i in qs:
		data = {'actor' : i.cast.cast_name,
				'director' : i.director.director}
		res.append(data)

	context = {
		'act_dir' : res
	}

	return render(request, 'act_dir.html', context)

def castCrew_other(request):

	qs = Movies.objects.all()
	only_crew = []
	result = ''
	for ele in qs: 
		all_cast = (ele.cast.cast_name) 
		all_cast = all_cast.split(',') 
		all_crew = ele.crew 
		movie_name = ele.title
		lang = ele.language
		for i in all_cast: 
			all_crew = all_crew.replace(i, '') 
		only_crew.append((movie_name, all_crew, lang))

	lang = Movies.objects.values('language').distinct()
	qs = Movies.objects.all()
	imdb =[]
	act_movie = defaultdict(lambda : 0)
	for ele in qs:
		all_cast = ele.cast.cast_name
		all_cast = all_cast.split(',')
		for leads in all_cast:
			#print(leads)
			for itr in only_crew:
				if ele.title != itr[0] and leads in itr[1]:
					if len(result) == 0:
						result += itr[0]+','+leads+ ','+str(ele.language)
					else:
						result += ';' + itr[0]+','+leads +','+ str(ele.language)

					
					if act_movie[(leads,itr[0])] == 0:
						data = {"movie":itr[0],
								"actor" : leads,
								"lang" : itr[2]
								}
						imdb.append(data)
						act_movie[(leads,itr[0])] += 1
					# movie.append(itr[0])
					# actor.append(leads)
					# lan.append(ele.language)

	result  = result.split(';')
	context = {
		'castCrew_other' : imdb,
		'castCrew_other1' : imdb
	}

	return render(request, 'castCrew_other.html', context)

def castCrew_same(request):

	qs = Movies.objects.all()
	only_crew = []
	result = ''
	for ele in qs: 
		all_cast = (ele.cast.cast_name) 
		all_cast = all_cast.split(',') 
		all_crew = ele.crew 
		movie_name = ele.title
		for i in all_cast: 
			all_crew = all_crew.replace(i, '') 
		only_crew.append((movie_name, all_crew))

	qs = Movies.objects.all()
	for ele in qs:
		all_cast = ele.cast.cast_name
		all_cast = all_cast.split(',')
		for leads in all_cast:
			#print(leads)
			for itr in only_crew:
				#print('yes')
				if ele.title == itr[0] and leads in itr[1]:
					print('yes')
					if len(result) == 0:
						result += itr[0]+','+leads
					else:
						result += ';' + itr[0]+','+leads
					break

	context = {
		'castCrew_same' : result
	}

	return render(request, 'castCrew_same.html', context)
