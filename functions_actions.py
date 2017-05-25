import random
import copy


class ActionFunctions:

	def action_grade_calculator(links, issue, parameter, agents, affiliation_weights):

		if (links.agent1 == agents and type(links.agent2).__name__ == 'Policymakers') or (links.agent2 == agents and type(links.agent1).__name__ == 'Policymakers'):
			actionWeight = 1
		else:
			actionWeight = 0.95

		# if typeAction == 'team':

		if links.agent1 == agents:

			if links.agent1.affiliation == links.agent2.affiliation:
				grade = links.conflict_level[0][issue][parameter] * links.aware * actionWeight

			# Affiliation 1-2
			if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
				(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
				grade = links.conflict_level[0][issue][parameter] * links.aware * actionWeight * affiliation_weights[0]

			# Affiliation 1-3
			if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
				(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
				grade = links.conflict_level[0][issue][parameter] * links.aware * actionWeight * affiliation_weights[1]

			# Affiliation 2-3
			if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
				(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
				grade = links.conflict_level[0][issue][parameter] * links.aware * actionWeight * affiliation_weights[2]

		if links.agent2 == agents:

			# Same affiliation
			if links.agent1.affiliation == links.agent2.affiliation:
				grade = links.conflict_level[1][issue][parameter] * links.aware * actionWeight

			# Affiliation 1-2
			if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
				(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
				grade = links.conflict_level[1][issue][parameter] * links.aware * actionWeight * affiliation_weights[0]

			# Affiliation 1-3
			if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
				(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
				grade = links.conflict_level[1][issue][parameter] * links.aware * actionWeight * affiliation_weights[1]

			# Affiliation 2-3
			if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
				(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
				grade = links.conflict_level[1][issue][parameter] * links.aware * actionWeight * affiliation_weights[2]

		return grade

	def action_grade_calculator_3S_AS(links, impact, agents, affiliation_weights, conflict_level_coef):

		if (links.agent1 == agents and type(links.agent2).__name__ == 'Policymakers') or (links.agent2 == agents and type(links.agent1).__name__ == 'Policymakers'):
			actionWeight = 1
		else:
			actionWeight = 0.95

		# Checking which agent in the link is the original agent
		if links.agent1 == agents:

			check_none = 0
			if agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][impact] == None:
				agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][impact] = 0
				check_none = 1

			belief_diff = abs(agents.belieftree_policy[0][agents.select_policy_3S_as][impact] - agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][impact])

			if check_none == 1:
				agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][impact] = None

		# Checking which agent in the link is the original agent
		if links.agent2 == agents:

			check_none = 0
			if agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][impact] == None:
				agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][impact] = 0
				check_none = 1

			belief_diff = abs(agents.belieftree_policy[0][agents.select_policy_3S_as][impact] - agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][impact])

			if check_none == 1:
				agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][impact] = None

		# Defining the conflict level
		if belief_diff <= 0.25:
			conflict_level_impact = conflict_level_coef[0]
		if belief_diff > 0.25 and belief_diff <= 1.75:
			conflict_level_impact = conflict_level_coef[2]
		if belief_diff > 1.75:
			conflict_level_impact = conflict_level_coef[1]

		# Same affiliation
		if links.agent1.affiliation == links.agent2.affiliation:
			grade = conflict_level_impact * links.aware * actionWeight

		# Affiliation 1-2
		if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
			grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[0]

		# Affiliation 1-3
		if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
			grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[1]

		# Affiliation 2-3
		if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
			grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[2]

		return grade

	def action_grade_calculator_3S_PF(links, impact, agents, affiliation_weights, conflict_level_coef):

		if (links.agent1 == agents and type(links.agent2).__name__ == 'Policymakers') or (links.agent2 == agents and type(links.agent1).__name__ == 'Policymakers'):
			actionWeight = 1
		else:
			actionWeight = 0.95

		# Checking which agent in the link is the original agent
		if links.agent1 == agents:

			check_none = 0
			if agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][impact] == None:
				agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][impact] = 0
				check_none = 1

			belief_diff = abs(agents.belieftree_instrument[0][agents.select_policy_3S_pf][impact] - agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][impact])

			if check_none == 1:
				agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][impact] = None

		# Checking which agent in the link is the original agent
		if links.agent2 == agents:

			check_none = 0
			if agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][impact] == None:
				agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][impact] = 0
				check_none = 1

			belief_diff = abs(agents.belieftree_instrument[0][agents.select_policy_3S_pf][impact] - agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][impact])

			if check_none == 1:
				agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][impact] = None

		if belief_diff <= 0.25:
			conflict_level_impact = conflict_level_coef[0]
		if belief_diff > 0.25 and belief_diff <= 1.75:
			conflict_level_impact = conflict_level_coef[2]
		if belief_diff > 1.75:
			conflict_level_impact = conflict_level_coef[1]

		# Grade calculation using the likelihood method
		# Same affiliation
		if links.agent1.affiliation == links.agent2.affiliation:
			grade = conflict_level_impact * links.aware * actionWeight

		# Affiliation 1-2
		if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
			grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[0]

		# Affiliation 1-3
		if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
			grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[1]

		# Affiliation 2-3
		if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
			grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[2]

		return grade

<<<<<<< Updated upstream
	def action_implementor(links, issue, parameter, agents, agents_resources, affiliation_weights, resources_weight_action, resources_potency, blanket, action_agent_number):
=======
	def partial_knowledge_transfer(self, agent1, agent2, issue, parameter):

		agent1.belieftree[1 + agent2.unique_id][issue][parameter] = agent2.belieftree[0][issue][parameter] + (random.random()/5) - 0.1
		agent1.belieftree[1 + agent2.unique_id][issue][parameter] = self.one_minus_one_check(agent1.belieftree[1 + agent2.unique_id][issue][parameter])
		# Partial knowledge 2 with 1-1 check
		agent2.belieftree[1 + agent1.unique_id][issue][parameter] = agent1.belieftree[0][issue][parameter] + (random.random()/5) - 0.1
		agent2.belieftree[1 + agent1.unique_id][issue][parameter] = self.one_minus_one_check(agent2.belieftree[1 + agent1.unique_id][issue][parameter])

		results = [agent2.belieftree[0][issue][parameter], agent1.belieftree[1 + agent2.unique_id][issue][parameter], agent2.belieftree[1 + agent1.unique_id][issue][parameter]]
		print(results)

	def action_implementor(self, links, issue, parameter, agents, affiliation_weights, resources_weight_action, resources_potency, blanket, action_agent_number):
>>>>>>> Stashed changes

		if blanket == True:
			resources_potency = resources_potency / action_agent_number

		if links.agent1 == agents:
			
			# print('Before: ', links.agent2.belieftree[0][issue][parameter])

			# Same affiliation
			if links.agent1.affiliation == links.agent2.affiliation:
				links.agent2.belieftree[0][issue][parameter] += (agents.belieftree[0][issue][parameter] - links.agent2.belieftree[0][issue][parameter]) * \
					agents_resources.resources[0] * resources_weight_action * resources_potency

			# Affiliation 1-2
			if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
				links.agent2.belieftree[0][issue][parameter] += (agents.belieftree[0][issue][parameter] - links.agent2.belieftree[0][issue][parameter]) * \
					agents_resources.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

			# Affiliation 1-3
			if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
				links.agent2.belieftree[0][issue][parameter] += (agents.belieftree[0][issue][parameter] - links.agent2.belieftree[0][issue][parameter]) * \
					agents_resources.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

			# Affiliation 2-3
			if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
				links.agent2.belieftree[0][issue][parameter] += (agents.belieftree[0][issue][parameter] - links.agent2.belieftree[0][issue][parameter]) * \
					agents_resources.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

			# print('After: ', links.agent2.belieftree[0][issue][parameter])

			# Checks and transfer of partial knowledge
			# 1-1 check - new value
			links.agent2.belieftree[0][issue][parameter] = ActionFunctions.one_minus_one_check(links.agent2.belieftree[0][issue][parameter])
			# Partial knowledge 1 with 1-1 check
			agents.belieftree[1 + links.agent2.unique_id][issue][parameter] = links.agent2.belieftree[0][issue][parameter] + (random.random()/5) - 0.1
			agents.belieftree[1 + links.agent2.unique_id][issue][parameter] = ActionFunctions.one_minus_one_check(agents.belieftree[1 + links.agent2.unique_id][issue][parameter])
			# Partial knowledge 2 with 1-1 check
			links.agent2.belieftree[1 + agents.unique_id][issue][parameter] = agents.belieftree[0][issue][parameter] + (random.random()/5) - 0.1
			links.agent2.belieftree[1 + agents.unique_id][issue][parameter] = ActionFunctions.one_minus_one_check(links.agent2.belieftree[1 + agents.unique_id][issue][parameter])

			results = [links.agent2.belieftree[0][issue][parameter], agents.belieftree[1 + links.agent2.unique_id][issue][parameter], links.agent2.belieftree[1 + agents.unique_id][issue][parameter]]

		if links.agent2 == agents:

			# print('Before: ', links.agent1.belieftree[0][issue][parameter])
			
			# Same affiliation
			if links.agent1.affiliation == links.agent2.affiliation:
				links.agent1.belieftree[0][issue][parameter] += (agents.belieftree[0][issue][parameter] - links.agent1.belieftree[0][issue][parameter]) * \
					agents_resources.resources[0] * resources_weight_action * resources_potency

			# Affiliation 1-2
			if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
				links.agent1.belieftree[0][issue][parameter] += (agents.belieftree[0][issue][parameter] - links.agent1.belieftree[0][issue][parameter]) * \
					agents_resources.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

			# Affiliation 1-3
			if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
				links.agent1.belieftree[0][issue][parameter] += (agents.belieftree[0][issue][parameter] - links.agent1.belieftree[0][issue][parameter]) * \
					agents_resources.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

			# Affiliation 2-3
			if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
				links.agent1.belieftree[0][issue][parameter] += (agents.belieftree[0][issue][parameter] - links.agent1.belieftree[0][issue][parameter]) * \
					agents_resources.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

			# print('After: ', links.agent1.belieftree[0][issue][parameter])
			
			# Checks and transfer of partial knowledge
			# 1-1 check - new value
<<<<<<< Updated upstream
			links.agent1.belieftree[0][issue][parameter] = ActionFunctions.one_minus_one_check(links.agent1.belieftree[0][issue][parameter])
			# Partial knowledge 1 with 1-1 check
			agents.belieftree[1 + links.agent1.unique_id][issue][parameter] = links.agent1.belieftree[0][issue][parameter] + (random.random()/5) - 0.1
			agents.belieftree[1 + links.agent1.unique_id][issue][parameter] = ActionFunctions.one_minus_one_check(agents.belieftree[1 + links.agent1.unique_id][issue][parameter])
			# Partial knowledge 2 with 1-1 check
			links.agent1.belieftree[1 + agents.unique_id][issue][parameter] = agents.belieftree[0][issue][parameter] + (random.random()/5) - 0.1
			links.agent1.belieftree[1 + agents.unique_id][issue][parameter] = ActionFunctions.one_minus_one_check(links.agent1.belieftree[1 + agents.unique_id][issue][parameter])
=======
			links.agent1.belieftree[0][issue][parameter] = self.one_minus_one_check(links.agent1.belieftree[0][issue][parameter])

			partial_knowledge = self.partial_knowledge_transfer(links.agent2, links.agent1, issue, parameter)


			# # Partial knowledge 1 with 1-1 check
			# agents.belieftree[1 + links.agent1.unique_id][issue][parameter] = links.agent1.belieftree[0][issue][parameter] + (random.random()/5) - 0.1
			# agents.belieftree[1 + links.agent1.unique_id][issue][parameter] = self.one_minus_one_check(agents.belieftree[1 + links.agent1.unique_id][issue][parameter])
			# # Partial knowledge 2 with 1-1 check
			# links.agent1.belieftree[1 + agents.unique_id][issue][parameter] = agents.belieftree[0][issue][parameter] + (random.random()/5) - 0.1
			# links.agent1.belieftree[1 + agents.unique_id][issue][parameter] = self.one_minus_one_check(links.agent1.belieftree[1 + agents.unique_id][issue][parameter])
>>>>>>> Stashed changes

			results = [links.agent1.belieftree[0][issue][parameter], agents.belieftree[1 + links.agent1.unique_id][issue][parameter], links.agent1.belieftree[1 + agents.unique_id][issue][parameter]]
		
		return results

	def action_implementor_3S_AS(links, instrument, impact, agents, agents_resources, affiliation_weights, resources_weight_action, resources_potency, blanket, action_agent_number):

		# agents.select_policy_3S_as
		
		if blanket == True:
			resources_potency = resources_potency / action_agent_number

		if links.agent1 == agents:
			
			# print('Before: ', links.agent2.belieftree_policy[0][instrument][impact])

			# Same affiliation
			if links.agent1.affiliation == links.agent2.affiliation:
				links.agent2.belieftree_policy[0][instrument][impact] += (agents.belieftree_policy[0][instrument][impact] - links.agent2.belieftree_policy[0][instrument][impact]) * \
					agents_resources.resources[0] * resources_weight_action * resources_potency

			# Affiliation 1-2
			if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
				links.agent2.belieftree_policy[0][instrument][impact] += (agents.belieftree_policy[0][instrument][impact] - links.agent2.belieftree_policy[0][instrument][impact]) * \
					agents_resources.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

			# Affiliation 1-3
			if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
				links.agent2.belieftree_policy[0][instrument][impact] += (agents.belieftree_policy[0][instrument][impact] - links.agent2.belieftree_policy[0][instrument][impact]) * \
					agents_resources.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

			# Affiliation 2-3
			if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
				links.agent2.belieftree_policy[0][instrument][impact] += (agents.belieftree_policy[0][instrument][impact] - links.agent2.belieftree_policy[0][instrument][impact]) * \
					agents_resources.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

			# print('After: ', links.agent2.belieftree_policy[0][instrument][impact])

			# Checks and transfer of partial knowledge
			# 1-1 check - new value
			links.agent2.belieftree_policy[0][instrument][impact] = ActionFunctions.one_minus_one_check(links.agent2.belieftree_policy[0][instrument][impact])
			# Partial knowledge 1 with 1-1 check
			agents.belieftree_policy[1 + links.agent2.unique_id][instrument][impact] = links.agent2.belieftree_policy[0][instrument][impact] + (random.random()/5) - 0.1
			agents.belieftree_policy[1 + links.agent2.unique_id][instrument][impact] = ActionFunctions.one_minus_one_check(agents.belieftree_policy[1 + links.agent2.unique_id][instrument][impact])
			# Partial knowledge 2 with 1-1 check
			links.agent2.belieftree_policy[1 + agents.unique_id][instrument][impact] = agents.belieftree_policy[0][instrument][impact] + (random.random()/5) - 0.1
			links.agent2.belieftree_policy[1 + agents.unique_id][instrument][impact] = ActionFunctions.one_minus_one_check(links.agent2.belieftree_policy[1 + agents.unique_id][instrument][impact])

			results = [links.agent2.belieftree_policy[0][instrument][impact], agents.belieftree_policy[1 + links.agent2.unique_id][instrument][impact], \
				links.agent2.belieftree_policy[1 + agents.unique_id][instrument][impact]]

		if links.agent2 == agents:

			# print('Before: ', links.agent1.belieftree_policy[0][instrument][impact])
			
			# Same affiliation
			if links.agent1.affiliation == links.agent2.affiliation:
				links.agent1.belieftree_policy[0][instrument][impact] += (agents.belieftree_policy[0][instrument][impact] - links.agent1.belieftree_policy[0][instrument][impact]) * \
					agents_resources.resources[0] * resources_weight_action * resources_potency

			# Affiliation 1-2
			if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
				links.agent1.belieftree_policy[0][instrument][impact] += (agents.belieftree_policy[0][instrument][impact] - links.agent1.belieftree_policy[0][instrument][impact]) * \
					agents_resources.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

			# Affiliation 1-3
			if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
				links.agent1.belieftree_policy[0][instrument][impact] += (agents.belieftree_policy[0][instrument][impact] - links.agent1.belieftree_policy[0][instrument][impact]) * \
					agents_resources.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

			# Affiliation 2-3
			if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
				links.agent1.belieftree_policy[0][instrument][impact] += (agents.belieftree_policy[0][instrument][impact] - links.agent1.belieftree_policy[0][instrument][impact]) * \
					agents_resources.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

			# print('After: ', links.agent1.belieftree_policy[0][instrument][impact])
			
			# Checks and transfer of partial knowledge
			# 1-1 check - new value
			links.agent1.belieftree_policy[0][instrument][impact] = ActionFunctions.one_minus_one_check(links.agent1.belieftree_policy[0][instrument][impact])
			# Partial knowledge 1 with 1-1 check
			agents.belieftree_policy[1 + links.agent1.unique_id][instrument][impact] = links.agent1.belieftree_policy[0][instrument][impact] + (random.random()/5) - 0.1
			agents.belieftree_policy[1 + links.agent1.unique_id][instrument][impact] = ActionFunctions.one_minus_one_check(agents.belieftree_policy[1 + links.agent1.unique_id][instrument][impact])
			# Partial knowledge 2 with 1-1 check
			links.agent1.belieftree_policy[1 + agents.unique_id][instrument][impact] = agents.belieftree_policy[0][instrument][impact] + (random.random()/5) - 0.1
			links.agent1.belieftree_policy[1 + agents.unique_id][instrument][impact] = ActionFunctions.one_minus_one_check(links.agent1.belieftree_policy[1 + agents.unique_id][instrument][impact])

			results = [links.agent1.belieftree_policy[0][instrument][impact], agents.belieftree_policy[1 + links.agent1.unique_id][instrument][impact], \
				links.agent1.belieftree_policy[1 + agents.unique_id][instrument][impact]]
		
		return results

	def action_implementor_3S_PF(links, instrument, impact, agents, agents_resources, affiliation_weights, resources_weight_action, resources_potency, blanket, action_agent_number):

		# agents.select_policy_3S_pf
		if blanket == True:
			resources_potency = resources_potency / action_agent_number

		if links.agent1 == agents:
			
			# print('Before: ', links.agent2.belieftree_instrument[0][instrument][impact])

			# Same affiliation
			if links.agent1.affiliation == links.agent2.affiliation:
				links.agent2.belieftree_instrument[0][instrument][impact] += (agents.belieftree_instrument[0][instrument][impact] - links.agent2.belieftree_instrument[0][instrument][impact]) * \
					agents_resources.resources[0] * resources_weight_action * resources_potency

			# Affiliation 1-2
			if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
				links.agent2.belieftree_instrument[0][instrument][impact] += (agents.belieftree_instrument[0][instrument][impact] - links.agent2.belieftree_instrument[0][instrument][impact]) * \
					agents_resources.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

			# Affiliation 1-3
			if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
				links.agent2.belieftree_instrument[0][instrument][impact] += (agents.belieftree_instrument[0][instrument][impact] - links.agent2.belieftree_instrument[0][instrument][impact]) * \
					agents_resources.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

			# Affiliation 2-3
			if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
				links.agent2.belieftree_instrument[0][instrument][impact] += (agents.belieftree_instrument[0][instrument][impact] - links.agent2.belieftree_instrument[0][instrument][impact]) * \
					agents_resources.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

			# print('After: ', links.agent2.belieftree_instrument[0][instrument][impact])

			# Checks and transfer of partial knowledge
			# 1-1 check - new value
			links.agent2.belieftree_instrument[0][instrument][impact] = ActionFunctions.one_minus_one_check(links.agent2.belieftree_instrument[0][instrument][impact])
			# Partial knowledge 1 with 1-1 check
			agents.belieftree_instrument[1 + links.agent2.unique_id][instrument][impact] = links.agent2.belieftree_instrument[0][instrument][impact] + (random.random()/5) - 0.1
			agents.belieftree_instrument[1 + links.agent2.unique_id][instrument][impact] = ActionFunctions.one_minus_one_check(agents.belieftree_instrument[1 + links.agent2.unique_id][instrument][impact])
			# Partial knowledge 2 with 1-1 check
			links.agent2.belieftree_instrument[1 + agents.unique_id][instrument][impact] = agents.belieftree_instrument[0][instrument][impact] + (random.random()/5) - 0.1
			links.agent2.belieftree_instrument[1 + agents.unique_id][instrument][impact] = ActionFunctions.one_minus_one_check(links.agent2.belieftree_instrument[1 + agents.unique_id][instrument][impact])

			results = [links.agent2.belieftree_instrument[0][instrument][impact], agents.belieftree_instrument[1 + links.agent2.unique_id][instrument][impact], \
				links.agent2.belieftree_instrument[1 + agents.unique_id][instrument][impact]]

		if links.agent2 == agents:

			# print('Before: ', links.agent1.belieftree_instrument[0][instrument][impact])
			
			# Same affiliation
			if links.agent1.affiliation == links.agent2.affiliation:
				links.agent1.belieftree_instrument[0][instrument][impact] += (agents.belieftree_instrument[0][instrument][impact] - links.agent1.belieftree_instrument[0][instrument][impact]) * \
					agents_resources.resources[0] * resources_weight_action * resources_potency

			# Affiliation 1-2
			if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
				links.agent1.belieftree_instrument[0][instrument][impact] += (agents.belieftree_instrument[0][instrument][impact] - links.agent1.belieftree_instrument[0][instrument][impact]) * \
					agents_resources.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

			# Affiliation 1-3
			if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
				links.agent1.belieftree_instrument[0][instrument][impact] += (agents.belieftree_instrument[0][instrument][impact] - links.agent1.belieftree_instrument[0][instrument][impact]) * \
					agents_resources.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

			# Affiliation 2-3
			if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
				links.agent1.belieftree_instrument[0][instrument][impact] += (agents.belieftree_instrument[0][instrument][impact] - links.agent1.belieftree_instrument[0][instrument][impact]) * \
					agents_resources.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

			# print('After: ', links.agent1.belieftree_instrument[0][instrument][impact])
			
			# Checks and transfer of partial knowledge
			# 1-1 check - new value
			links.agent1.belieftree_instrument[0][instrument][impact] = ActionFunctions.one_minus_one_check(links.agent1.belieftree_instrument[0][instrument][impact])
			# Partial knowledge 1 with 1-1 check
			agents.belieftree_instrument[1 + links.agent1.unique_id][instrument][impact] = links.agent1.belieftree_instrument[0][instrument][impact] + (random.random()/5) - 0.1
			agents.belieftree_instrument[1 + links.agent1.unique_id][instrument][impact] = ActionFunctions.one_minus_one_check(agents.belieftree_instrument[1 + links.agent1.unique_id][instrument][impact])
			# Partial knowledge 2 with 1-1 check
			links.agent1.belieftree_instrument[1 + agents.unique_id][instrument][impact] = agents.belieftree_instrument[0][instrument][impact] + (random.random()/5) - 0.1
			links.agent1.belieftree_instrument[1 + agents.unique_id][instrument][impact] = ActionFunctions.one_minus_one_check(links.agent1.belieftree_instrument[1 + agents.unique_id][instrument][impact])

			results = [links.agent1.belieftree_instrument[0][instrument][impact], agents.belieftree_instrument[1 + links.agent1.unique_id][instrument][impact], \
				links.agent1.belieftree_instrument[1 + agents.unique_id][instrument][impact]]
		
		return results

	def one_minus_one_check(to_be_checked_parameter):

		"""
		One minus one check function
		===========================

		This function checks that a certain values does not got over one
		and does not go below one due to the randomisation.
		
		"""

		checked_parameter = 0
		if to_be_checked_parameter > 1:
			checked_parameter = 1
		elif to_be_checked_parameter < -1:
			checked_parameter = -1
		else:
			checked_parameter = to_be_checked_parameter
		return checked_parameter

