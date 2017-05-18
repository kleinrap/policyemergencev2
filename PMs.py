import random
import copy

class Policymakers(Agent):

	def __init__(self, run_number, agent_id, unique_id, pos, network_strategy, affiliation, resources, belieftree, instrument_preferences, belieftree_policy, belieftree_instrument, select_as_issue, select_pinstrument, select_issue_3S_as, \
		select_problem_3S_as, select_policy_3S_as, select_issue_3S_pf, select_problem_3S_pf, select_policy_3S_pf, team_as, team_pf, coalition_as, coalition_pf):
		# super().__init__(unique_id, model)
		self.run_number = run_number
		self.agent_id = agent_id
		self.pos = pos
		self.network_strategy = network_strategy
		self.unique_id = unique_id
		# self.model = model
		self.affiliation = affiliation
		self.resources = resources
		self.belieftree = belieftree
		self.belieftree_policy = belieftree_policy
		self.belieftree_instrument = belieftree_instrument
		self.instrument_preferences = instrument_preferences
		self.select_as_issue = select_as_issue
		self.select_pinstrument = select_pinstrument
		self.select_issue_3S_as = select_issue_3S_as
		self.select_problem_3S_as = select_problem_3S_as
		self.select_policy_3S_as = select_policy_3S_as
		self.select_issue_3S_pf = select_issue_3S_pf
		self.select_problem_3S_pf = select_problem_3S_pf
		self.select_policy_3S_pf = select_policy_3S_pf
		self.team_as = team_as
		self.team_pf = team_pf
		self.coalition_as = coalition_as
		self.coalition_pf = coalition_pf

	# def __str__(self):
	# 	return 'POLICYMAKER - Affiliation: ' + str(self.affiliation) + ', Resources: ' + str(self.resources) + \
	# 	', Position: [' + str(self.pos[0]) + ',' + str(self.pos[1]) + '], ID: ' + str(self.unique_id) + \
	# 	', Problem selected: ' + str(self.select_problem) + ', Policy selected: ' + str(self.select_policy) + \
	# 	', Belief tree: ' + str(self.belieftree)



	# Simple print with ID
	def __str__(self):
		return 'Policy maker: ' + str(self.unique_id)

	def policymakers_states_update(self, agent, master_list, affiliation_weights):

		"""
		The policy makers states update function
		===========================

		This function uses the data from the external parties to update the states of 
		the policy makers.

		Note: Ultimately, this would need to include the external parties lack of interests
		for some of the states.

		"""

		#' Addition of more than 3 affiliation will lead to unreported errors!')
		if len(affiliation_weights) != 3:
			print('WARNING - THIS CODE DOESNT WORK FOR MORE OR LESS THAN 3 AFFILIATIONS')

		# Defining the external party list along with the truth agent relation
		externalparties_list = []
		for agents in master_list:
			if type(agents) == Truth:
				truthagent = agents
			if type(agents) == Externalparties:
				externalparties_list.append(agents)

		# going through the different external parties:
		belief_sum_ep = [0 for k in range(len(truthagent.belieftree_truth))]
		# print(belief_sum_ep)
		for i in range(len(truthagent.belieftree_truth)):
			# print('NEW ISSUE! NEW ISSUES!')
			# This is used because in some cases, the external parties will have no impact on the agent (None values in the states of the EP)
			actual_length_ep = 0
			for j in range(len(externalparties_list)):
				# This line is added in case the EP has None states
				if externalparties_list[j].belieftree[0][i][0] != 'No':
					actual_length_ep += 1
					# Currently, the state of the policy makers is initialised as being equal to their initial aim:
					if agent.belieftree[0][i][0] == None:
						# print('Triggered - changed to: ' + str(agent.belieftree[0][i][1]))
						agent.belieftree[0][i][0] = agent.belieftree[0][i][1]
					# If they have the same affiliation, add without weight
					if externalparties_list[j].affiliation == agent.affiliation:
						# print('AFFILIATIONS ARE EQUAL')
						# print('issue ' + str(i+1) + ': ' + str(externalparties_list[j].belieftree[0][i][0]) +  /
						# ' and affiliation: ' + str(externalparties_list[j].affiliation) + '  ' + str(externalparties_list[j].unique_id))
						# print('This is the sum: ' + str(belief_sum_ep[i]))
						belief_sum_ep[i] = belief_sum_ep[i] + (externalparties_list[j].belieftree[0][i][0] - agent.belieftree[0][i][0])
						# print('The sum is equal to: ' + str(belief_sum_ep))
						# print('The change in state belief is equal to: ' + str(belief_sum_ep[i] / len(externalparties_list)))
					if (externalparties_list[j].affiliation == 0 and agent.affiliation == 1) or \
					   (externalparties_list[j].affiliation == 1 and agent.affiliation == 0):
						# print('AFFILIATION 1 AND 2')
						belief_sum_ep[i] = belief_sum_ep[i] + \
						   (externalparties_list[j].belieftree[0][i][0] - agent.belieftree[0][i][0]) * affiliation_weights[0]
					if (externalparties_list[j].affiliation == 0 and agent.affiliation == 2) or \
					   (externalparties_list[j].affiliation == 2 and agent.affiliation == 0):
						# print('AFFILIATION 1 AND 3')
						belief_sum_ep[i] = belief_sum_ep[i] + \
						   (externalparties_list[j].belieftree[0][i][0] - agent.belieftree[0][i][0]) * affiliation_weights[1]
					if (externalparties_list[j].affiliation == 1 and agent.affiliation == 2) or \
					   (externalparties_list[j].affiliation == 2 and agent.affiliation == 1):
						# print('AFFILIATION 2 AND 3')
						belief_sum_ep[i] = belief_sum_ep[i] + \
						   (externalparties_list[j].belieftree[0][i][0] - agent.belieftree[0][i][0]) * affiliation_weights[2]
			agent.belieftree[0][i][0] = agent.belieftree[0][i][0] + belief_sum_ep[i] / actual_length_ep
			# print('This is issue: ' + str(i+1) + ' and its new value is: ' + str(agent.belieftree[0][i][0]))
		# print(agent)