import csv


matches_fields = {}		# mapping of fields to numbers ('matches.csv')
no_result_id = []		# contains id's of matches with no result , a draw or a tie
needed_rows = []		# only required rows ('matches.csv')
needed_fields = []		# only required fields ('matches.csv')
teams_short = {}		# shortcuts for team names
d_needed_rows = []		# only required rows ('deliveries.csv')
d_needed_fields = []	# only required fields ('delivieries.csv')
d_match_fields = {}		# mapping of fields to numbers (deliveries.csv)
team_venue = {}			# teams - home grounds
team_num = {}			# teams - numbers
final_fields = []		# final required fields
final_rows = []			# final required data
final_match_fields = {}	# final mapping fields to numbers
test_rows = []			# subset of final rows for testing
train_rows = []			# subset of final rows for training


def matches_init():

	"""
	overall matches [ win , toss , venue , names-shortforms ]
	useful info for further use
	"""

	global no_result_id , matches_fields , needed_rows , needed_fields , teams_short

	filename = 'ipl/matches.csv'
	fields = []		# column fields
	rows = []		# column data

	# read complete 'matches' csv file
	with open(filename, 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		# take column fields first
		fields = next(csvreader)
		# take remaining data
		for row in csvreader:
			rows.append(row)
	csvfile.close()

	# keep only what is needed
	needed_fields = ['id' , 'season' , 'city' , 'date' , 'team1' , 'team2' , 'toss_winner' , 'toss_decision' , 'result' , 'winner' , 'venue']

	# assign names to numbers
	for i in range(0 , len(fields) , 1):
		matches_fields[fields[i]] = i

	# create shortcuts for team names
	team_names = ['Mumbai Indians','Kolkata Knight Riders','Royal Challengers Bangalore','Deccan Chargers','Chennai Super Kings','Rajasthan Royals','Delhi Daredevils','Gujarat Lions','Kings XI Punjab','Sunrisers Hyderabad','Rising Pune Supergiants','Rising Pune Supergiant','Kochi Tuskers Kerala','Pune Warriors']
	team_names_short = ['MI','KKR','RCB','SRH','CSK','RR','DD','GL','KXIP','SRH','RPS','RPS','KTK','PW']
	teams_short = dict(zip(team_names , team_names_short))
	for i in rows:
		if i[matches_fields['result']] == 'normal':
			for j in ['team1' , 'team2' , 'toss_winner' , 'winner']:
				i[matches_fields[j]] = teams_short[i[matches_fields[j]]]

	# working teams - we are working between only these teams
	wteams = ['MI' , 'KKR' , 'RCB' , 'SRH' , 'CSK' , 'RR' , 'DD' , 'KXIP']

	# get all not normal matches id's
	# excluding non working teams
	for i in range(0 , len(rows) , 1):
		tmp = rows[i][matches_fields['result']]
		if tmp == 'no result' or tmp == 'draw' or tmp == 'tie' or rows[i][matches_fields['team1']] not in wteams or rows[i][matches_fields['team2']] not in wteams:
			no_result_id.append(rows[i][0])
	no_result_id.append(120)	# less than 6 overs
	no_result_id.append(489)	# less than 6 overs
	no_result_id = list(map(int , no_result_id))

	# row data according to needed_fields
	# excluding no result matches
	for i in range(0 , len(rows) , 1):
		row = []
		if int(rows[i][0]) not in no_result_id:
			for j in needed_fields:
				row.append(rows[i][matches_fields[j]])
			needed_rows.append(row)

	# change matches fields
	for i in range(0 , len(needed_fields) , 1):
		matches_fields[needed_fields[i]] = i

	# -- got all required data till here --
	
	# change id & season to int
	for i in needed_rows:
		for j in [0 , 1]:
			i[j] = int(i[j])

	"""
	#testing
	print(needed_fields)
	print()
	for i in needed_rows[:5]:
		print(i)
	"""

def deliveries_init():

	filename = 'ipl/deliveries.csv'
	fields = []
	rows = []

	global d_needed_fields , d_needed_rows , d_match_fields , team_venue , team_num

	# read deliveries file
	with open(filename , 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		fields = next(csvreader)
		for i in csvreader:
			rows.append(i)

	# needed fields in deliveries.csv
	d_needed_fields = ['match_id' , 'inning' , 'batting_team' , 'bowling_team' , 'over' , 'ball' , 'batsman' , 'non_striker' , 'bowler' , 'batsman_runs' , 'total_runs' , 'player_dismissed']

	# assign names to numbers
	for i in range(0 , len(fields) , 1):
		d_match_fields[fields[i]] = i

	# get needed rows and needed cols
	for i in range(0 , len(rows) , 1):
		row = []
		if int(rows[i][0]) not in no_result_id:
			for j in d_needed_fields:
				row.append(rows[i][d_match_fields[j]])
			d_needed_rows.append(row)

	# reassign
	for i in range(0 , len(d_needed_fields) , 1):
		d_match_fields[d_needed_fields[i]] = i

	# player dismissed is wickets count
	for i in range(0 , len(d_needed_rows) , 1):
		if d_needed_rows[i][d_match_fields['player_dismissed']] != '':
			d_needed_rows[i][d_match_fields['player_dismissed']] = '1'
		else:
			d_needed_rows[i][d_match_fields['player_dismissed']] = '0'

	# change to int - required cols
	for i in range(0 , len(d_needed_rows) , 1):
		for j in ['match_id' , 'inning' , 'over' , 'ball' , 'batsman_runs' , 'total_runs' , 'player_dismissed']:
			d_needed_rows[i][d_match_fields[j]] = int(d_needed_rows[i][d_match_fields[j]])

	# cumulative runs and wickets
	for i in range(1 , len(d_needed_rows) , 1):
		if d_needed_rows[i][d_match_fields['inning']] == d_needed_rows[i - 1][d_match_fields['inning']]:
			d_needed_rows[i][d_match_fields['total_runs']] += d_needed_rows[i - 1][d_match_fields['total_runs']]
			d_needed_rows[i][d_match_fields['player_dismissed']] += d_needed_rows[i - 1][d_match_fields['player_dismissed']]


	# teams - home grounds
	home = [ 'Wankhede Stadium' , 'Eden Gardens' , 'M Chinnaswamy Stadium' , 'Rajiv Gandhi International Stadium, Uppal' , 'MA Chidambaram Stadium, Chepauk' , 'Sawai Mansingh Stadium' , 'Feroz Shah Kotla' , 'Punjab Cricket Association Stadium, Mohali']
	home_teams = ['MI' , 'KKR' , 'RCB' , 'SRH' , 'CSK' , 'RR' , 'DD' , 'KXIP']
	num = [[0,0,0,0,0,0,0,1] , [0,0,0,0,0,0,1,0] , [0,0,0,0,0,1,0,0] , [0,0,0,0,1,0,0,0] , [0,0,0,1,0,0,0,0] , [0,0,1,0,0,0,0,0] , [0,1,0,0,0,0,0,0] , [1,0,0,0,0,0,0,0]]
	team_venue = dict(zip(home_teams , home))
	team_num = dict(zip(home_teams , num))

	"""
	#testing
	for i in d_needed_rows[:500]:
		print(i)
	"""

def final_data():
	
	global final_fields , final_rows , final_match_fields
	global test_rows , train_rows , Xtrain , Ytrain , Xtest , Ytest

	final_fields = ['id' , 'inning' , 'batting_team' , 'bowling_team' , 'run_rate' , 'score' , 'wickets' , 'home_ground' , 'balls' , 'batting_order' , 'momentum' , 'total_balls' , 'target']

	# mapping
	for i in range(0 , len(final_fields) , 1):
		final_match_fields[final_fields[i]] = i

	cnt = 0
	for i in range(0 , len(d_needed_rows) , 1):
		if d_needed_rows[i][d_match_fields['over']] > 5:
			cnt += 1

	# final data required
	final_rows = []

	cnt = 0
	for i in range(0 , len(d_needed_rows) , 1):
		if d_needed_rows[i][d_match_fields['over']] > 5:
			row = [0] * len(final_fields)
			row[final_match_fields['id']] = d_needed_rows[i][d_match_fields['match_id']]
			row[final_match_fields['inning']] = d_needed_rows[i][d_match_fields['inning']]
			row[final_match_fields['batting_team']] = d_needed_rows[i][d_match_fields['batting_team']]
			row[final_match_fields['bowling_team']] = d_needed_rows[i][d_match_fields['bowling_team']]
			row[final_match_fields['score']] = d_needed_rows[i][d_match_fields['total_runs']]
			row[final_match_fields['wickets']] = d_needed_rows[i][d_match_fields['player_dismissed']]
			row[final_match_fields['balls']] = (d_needed_rows[i][d_match_fields['over']] - 1) * 6 + d_needed_rows[i][d_match_fields['ball']]
			row[final_match_fields['batting_order']] = 1 if d_needed_rows[i][d_match_fields['inning']] > 1 else 0
			row[final_match_fields['momentum']] = d_needed_rows[i][d_match_fields['total_runs']] - d_needed_rows[i - 30][d_match_fields['total_runs']]
			row[final_match_fields['run_rate']] = (float(row[final_match_fields['score']])/float(row[final_match_fields['balls']])) * 6.0
			final_rows.append(row)

	"""
	for i in final_rows[:300]:
		print(i)
	"""
	tmp_fields = ['id' , 'inning' , 'batting_team' , 'bowling_team' , 'venue' , 'total_balls' , 'target']
	tmp_rows = []
	cnt = 0
	for i in range(0 , len(d_needed_rows) , 1):
		if i == len(d_needed_rows) - 1 or d_needed_rows[i][d_match_fields['inning']] != d_needed_rows[i + 1][d_match_fields['inning']]:
			row = [0] * len(tmp_fields)
			row[0] = d_needed_rows[i][d_match_fields['match_id']]
			row[1] = d_needed_rows[i][d_match_fields['inning']]
			row[2] = d_needed_rows[i][d_match_fields['batting_team']]
			row[3] = d_needed_rows[i][d_match_fields['bowling_team']]
			row[4] = needed_rows[int(cnt/2)][matches_fields['venue']]
			row[5] = (d_needed_rows[i][d_match_fields['over']] - 1) * 6 + d_needed_rows[i][d_match_fields['ball']]
			row[6] = d_needed_rows[i][d_match_fields['total_runs']]
			tmp_rows.append(row)
			cnt += 1

	"""
	# testing
	for i in tmp_rows:
		print(i)
	print()
	"""

	cnt = -1
	for i in range(0 , len(final_rows) , 1):
		if i == 0 or final_rows[i][final_match_fields['inning']] != final_rows[i - 1][final_match_fields['inning']]:
			cnt += 1
		final_rows[i][final_match_fields['total_balls']] = tmp_rows[cnt][5]
		final_rows[i][final_match_fields['target']] = tmp_rows[cnt][6]
		final_rows[i][final_match_fields['home_ground']] = 1 if team_venue[teams_short[final_rows[i][final_match_fields['batting_team']]]] == tmp_rows[cnt][4] else 0
		final_rows[i][final_match_fields['batting_team']] = team_num[teams_short[final_rows[i][final_match_fields['batting_team']]]]
		final_rows[i][final_match_fields['bowling_team']] = team_num[teams_short[final_rows[i][final_match_fields['bowling_team']]]]

	# divide into test and train
	for i in range(0 , len(final_rows) , 1):
		if final_rows[i][final_match_fields['id']] > 59:
			train_rows.append(final_rows[i])
		else:
			test_rows.append(final_rows[i])
	# done

	# taking out match id & innings
	# for now taking out teams
	for i in range(0 , len(test_rows) , 1):
		test_rows[i] = test_rows[i][4:]
	for i in range(0 , len(train_rows) , 1):
		train_rows[i] = train_rows[i][4:]
	final_fields = final_fields[4:]
	for i in range(0 , len(final_fields) , 1):
		final_match_fields[final_fields[i]] = i
	# done

	# now write the train and test data in two different files
	with open('train_data.csv' , 'w') as csv_file:
		writer = csv.writer(csv_file , delimiter = ',' , lineterminator = '\n')
		#writer.writerow([str(j) for j in final_fields])
		for i in train_rows:
			writer.writerow([str(j) for j in i])
	csv_file.close()
	with open('test_data.csv' , 'w') as csv_file:
		writer = csv.writer(csv_file , delimiter = ',' , lineterminator = '\n')
		#writer.writerow([str(j) for j in final_fields])
		for i in test_rows:
			writer.writerow([str(j) for j in i])
	csv_file.close()

""" rough
	# divide into Xtrain , Ytrain & Xtest and Ytest
	for i in range(0 , len(train_rows) , 1):
		Xtrain.append(train_rows[i][:len(final_fields) - 1])
		Ytrain.append(train_rows[i][len(final_fields) - 1:])
	for i in range(0 , len(test_rows) , 1):
		Xtest.append(test_rows[i][:len(final_fields) - 1])
		Ytest.append(test_rows[i][len(final_fields) - 1:])

	Xtrain = np.array(Xtrain)
	Ytrain = np.array(Ytrain)
	Xtest = np.array(Xtest)
	Ytest = np.array(Ytest)

	# model
	knn = KNeighborsClassifier(n_neighbors=3)
	knn.fit(Xtrain , Ytrain)

"""

if __name__ == '__main__':
	
	# cleaning data thoroughly
	matches_init()
	deliveries_init()
	final_data()
