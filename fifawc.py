import csv
from dateutil.parser import parse

class Game:
	def __init__(this, date, home_team, away_team, home_score, away_score, tournament, city, country, isNeutral):
		d = parse(date, dayfirst=True)
	
		this.date = d
		this.year = d.year
		this.week = d.isocalendar()[1]
		this.home_team = home_team
		this.away_team = away_team
		this.home_score = home_score
		this.away_score = away_score
		this.tournament = tournament
		this.city = city
		this.country = country
		this.isNeutral = isNeutral

		
class Rating:
	
	def __init__(this, date, ratings):
	
		this.date = date
		this.ratings = ratings
		
games = []
ratings = []

def initGames():
	with open('results.csv') as resultsCsv:
		resultsRows = csv.reader(resultsCsv, delimiter=',')
		for row in resultsRows:
			date = row[0]
			home = row[1]
			away = row[2]
			home_score = int(row[3])
			away_score = int(row[4])
			tournament = row[5]
			city = row[6]
			country = row[7]
			isNeutral = row[8]

			games.append(Game(date, home, away, home_score, away_score, tournament, city, country, isNeutral))

def initRatings():
	with open('fifa_ranking.csv') as rankingsCsv:
		resultsRows = csv.reader(rankingsCsv, delimiter=',')

		month = {}
		
		curDate = None

		for row in resultsRows:
			date = parse(row[15])
			team = row[1]
			rank = int(row[0])
			rating = float(row[3])
			
			if curDate is None or curDate == date:
				month[team] = (rank, rating)
				curDate = date
			else:
				ratings.append(Rating(date, month))
				curDate = date
				month = {}
		
		# add the last month
		ratings.append(Rating(curDate, month))
			
def getRating(date, team, allRatings):
	for rating in reversed(allRatings):
		if rating.date <= date:
			if rating.ratings.has_key(team):
				return rating.ratings[team]
			else:
				return None
	
	raise Exception("rating not found: "+str(date))
	

initGames()
initRatings()
		
for game in games:
	
	home_rating = getRating(game.date, game.home_team, ratings)
	away_rating = getRating(game.date, game.away_team, ratings)
	
	if home_rating is not None and away_rating is not None:
		#print "%s %s, %s %s" % (game.home_team, str(home_rating), game.away_team, str(away_rating))
		
		rank_diff = home_rating[0] - away_rating[0]
		rating_diff = home_rating[1] - away_rating[1]
		
		print "%i, %d, %i, %i, %s" % (rank_diff, rating_diff, game.home_score, game.away_score, str(game.isNeutral))
	

