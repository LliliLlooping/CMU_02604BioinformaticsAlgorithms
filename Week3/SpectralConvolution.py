

def SpectralConvolution(spectrum):
    """
        Input: A collection of integers Spectrum.
        Output: The list of elements in the convolution of Spectrum. 
                If an element has multiplicity k, it should appear exactly k times; you may return the elements in any order.
    """
    # Sort the spectrum in ascending order
    spectrum = sorted(spectrum)

    # Get the number of intergers in the input spectrum
    lengthSpectrum = len(spectrum)

    # Every element subtract the elements on its left
    result = [spectrum[j] - spectrum[i]
              for i in range(lengthSpectrum - 1) for j in range(i+1, lengthSpectrum)]

    # Remove zeros from the result
    while 0 in result:
        result.remove(0)

    return sorted(result)

######################################################################
########################## Debugging Runs ############################
######################################################################


# spectrum = [0, 137, 186, 323]
# with open('input.txt', 'r') as file:
#     data = file.readline()
# spectrum = [eval(i) for i in data.split(' ')]
# result = SpectralConvolution(spectrum)
# s = ''
# for i in result:
#     s += str(i) + ' '
# print(s[:-1])
