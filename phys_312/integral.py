import doctest, math

def intg(f, xlo, xhi, tol=1e-5, print_progress=True, **kwargs):

	"""
	This is an function that computes the integral of a mathematical function to some degree of accuracy. 
	The input is a function f and the output is the
	approximated integral, appropriately called current_answer, as this method uses
	a Riemann Sum. Here is how it works:
	cut the area under the curve into tiny rectangles, computing the 
	contribution of each rectangle, and then summing the contributions


	Doctests:
	The purpose of these doctests is to check the calculations quickly.

	>>> (round(intg(f1, 0, math.pi, print_progress=False)[0], 6) == round(2, 6), intg(f1, 0, math.pi, print_progress=False)[1] < 1e-7)
	(True, True)

	>>> (round(intg(f2, 1, 3, print_progress=False)[0], 6) == round((1/math.exp(1) - 1/(math.exp(1))**3), 6), intg(f2, 1, 3, print_progress=False)[1] < 1e-7)
	(True, True)

  	If true, then the test fails and the fractional difference is greater than the tolerance. 
  	This comparison is what makes the program exit the calculation in the while loop.

    """

	# Initialization of variables
	t = kwargs["t"] if "t" in kwargs else None
	frac_diff = 1
	dx = 1
	x = xlo
	previous_answer = None
	current_answer = 0
	
	while frac_diff >= tol:

		number_of_steps = (xhi - xlo) / dx
		
		# Integral Calculation
		while x <= xhi:
			try:
				if t != None:
					current_answer += ((f(x, t) * dx)) # The Riemann Sum
				else:
					current_answer += (f(x) * dx)
			except ZeroDivisionError:
				current_answer += f(x+1e-9) * dx
			x += dx
		x = xlo

		# Fractional Difference
		if previous_answer is not None:
			frac_diff = abs((current_answer-previous_answer)/current_answer)
		else:
			frac_diff = "N/A"

		# Formating and printing the progress
		if print_progress:
			print(f"Number of steps: "+"{:.5g}".format(number_of_steps))
			print(f"dx =", "{:.5f},".format(dx), f"integral = "+"{:.8f}".format(current_answer))
			print(f"frac_diff = "+"{:.8f}".format(100*frac_diff)+"%\n") if previous_answer is not None \
				else print(f"frac_diff = {frac_diff}\n")

		# End steps (changes to previous/current answers and dx)
		if previous_answer is None:
			frac_diff = 1 # to keep the while loop alive
		previous_answer = current_answer
		if frac_diff >= tol:
			current_answer = 0
		dx = dx/2

	# Return statement
	return current_answer, frac_diff

# # Function 1
# f1 = lambda x : math.sin(x)

# # Function 2
# f2 = lambda z : math.exp(-z)

# # Function 3
# f3 = lambda y : (y**3) / (math.exp(y) -1)

# #Error Function
# f4 = lambda t : (2*(math.pi**(1/2)))*math.exp(-(t**2))

# # Function 5
# f5 = lambda t : 2*t

if __name__ == "__main__":

	print(f"running...")

	doctest.testmod()

	calculated_result, frac_diff = intg(f5, 1, 3)
	actual_result = 8
	actual_fractional_error = (actual_result-calculated_result)/(actual_result)
	print(f"The integral evaluated to within specified accuracy: "+"{:.8f}".format(calculated_result))
	print(f"The upper limit of its fractional error is estimated to be: "+"{:.8f}".format(100*frac_diff)+"%")
	print(f"The analytically calculated correct answer is: "+"{:.8f}".format(actual_result))
	print(f"The actual fractional error is: "+"{:.8f}".format(100*(actual_fractional_error))+"%")