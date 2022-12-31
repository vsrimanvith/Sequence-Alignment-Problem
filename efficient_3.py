import sys
import time
import psutil

first_line = ''
second_line = ''
alpha_values = {}

def setValuesOfAlpha ():
    alpha_values['A'] = {"A" : 0, "C" : 110, "G" : 48, "T": 94}
    alpha_values['C'] = {"A" : 110, "C" : 0, "G" : 118, "T": 48}
    alpha_values['G'] = {"A" : 48, "C" : 118, "G" : 0, "T": 110}
    alpha_values['T'] = {"A" : 94, "C" : 48, "G" : 110, "T": 0}

def generateString (given_string, indices):
    final_string = given_string
    for i in range (0, len (indices)):
        idx = int(indices[i])
        before_idx = final_string[:idx+1]
        after_idx = final_string[idx+1:]
        final_string = before_idx + final_string + after_idx

    return final_string

def formInputStrings (fileName):
    global first_line, second_line
    
    with open(fileName, 'r') as file:
        lines = file.readlines()
    file.close ()

    first_string_indices = []
    second_string_indices = []

    for line in lines:
        line = line.strip("\n")
        if not line.isdigit ():
            if len(first_line) == 0:
                first_line = line
            else:
                second_line = line
        else:
            if len(second_line) == 0:
                first_string_indices.append(line)
            else:
                second_string_indices.append(line)

    first_line = generateString(first_line, first_string_indices)
    second_line = generateString(second_line, second_string_indices)

    setValuesOfAlpha()

def basicApproach (first_string, second_string, alphaVal, deltaVal):
    result_string_1 = ""
    result_string_2 = ""

    m = len (first_string)
    n = len (second_string)

    dp = [[0 for i in range (n + 1)] for i in range (m + 1)]

    for i in range (m + 1):
        dp[i][0] = i * deltaVal

    for j in range (n + 1):
        dp[0][j] = j * deltaVal

    for i in range (1, m + 1):
        for j in range (1, n + 1):
            w1 = first_string[i - 1]
            w2 = second_string[j - 1]
            alpha = alphaVal[w1][w2]

            dp[i][j] = min (dp[i - 1][j - 1] + alpha, dp[i-1][j] + deltaVal, dp[i][j - 1] + deltaVal)

    i = n
    j = m

    while i > 0 and j > 0:
        diag = dp[j - 1][i - 1] + alphaVal[first_string[j - 1]][second_string[i - 1]]
        left = dp[j][i - 1] + deltaVal

        if dp[j][i] == diag:
            result_string_1 += first_string[j - 1]
            result_string_2 += second_string[i - 1]
            i -= 1
            j -= 1

        elif dp[j][i] == left:
            result_string_1 += '_'
            result_string_2 += second_string[i-1]
            i -= 1

        else:
            result_string_1 += first_string[j-1]
            result_string_2 += '_'
            j -= 1

    while j > 0:
        result_string_1 += first_string[j - 1]
        result_string_2 += '_'
        j -= 1

    while i > 0:
        result_string_1 += '_'
        result_string_2 += second_string[i-1]
        i -= 1

    result_string_1 = result_string_1[::-1]
    result_string_2 = result_string_2[::-1]

    return [result_string_1, result_string_2, dp[m][n]]

def spaceEfficientMethod (string1, string2, alphaValue, deltaValue):
    m = len (string1)
    n = len (string2)

    dp = [[0 for _ in range (2)] for _ in range (n + 1)]

    for i in range (0, n + 1):
        dp[i][0] = i * deltaValue

    for j in range (1, m + 1):
        dp[0][1] = j * deltaValue

        for i in range (1, n + 1):
            w1 = string1[j - 1]
            w2 = string2[i - 1]

            alpha = alphaValue[w1][w2]

            dp[i][1] = min (dp[i-1][0] + alpha, dp[i - 1][1] + deltaValue, dp[i][0] + deltaValue)

        for i in range (0,n + 1):
            dp[i][0] = dp[i][1]

    return dp

efficient_string_1 = ''
efficient_string_2 = ''
efficient_val = 0

def efficientApproach (first_string, second_string, alphaValue, deltaValue):
    global efficient_string_1, efficient_string_2, efficient_val
    m = len (first_string)
    n = len (second_string)

    if m <= 2 or n <= 2:
        ret = basicApproach(first_string, second_string, alphaValue, deltaValue)
        res1, res2 = ret[0], ret[1]

        efficient_string_1 += res1
        efficient_string_2 += res2
        efficient_val += ret[2]

        return

    first_x = first_string[:m//2+1]
    last_x = first_string[m//2+1:]

    dp = spaceEfficientMethod(first_x, second_string, alphaValue, deltaValue)

    last_x_reverse = last_x[::-1]
    Y_reverse = second_string[::-1]

    reverse_dp = spaceEfficientMethod(last_x_reverse, Y_reverse, alphaValue, deltaValue)

    min_idx = -1
    min_val = float('inf')

    for i in range (0, n + 1):

        if min_val > (dp[i][1] + reverse_dp[n - i][1]):
            min_val = dp[i][1] + reverse_dp[n - i][1]
            min_idx = i

    first_y = second_string[:min_idx]
    last_y = second_string[min_idx:]
    
    efficientApproach(first_x, first_y, alphaValue, deltaValue)
    efficientApproach(last_x, last_y, alphaValue, deltaValue)

def efficientDPApproach ():
    givenFileInput = sys.argv[1]
    start_time = time.time()
    process = psutil.Process()

    formInputStrings (givenFileInput)
    alpha = alpha_values
    delta = 30
    first_string = first_line
    second_string =  second_line    

    efficientApproach(first_string, second_string, alpha, delta)

    end_time = time.time()
    time_taken = (end_time - start_time)*1000

    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)

    with open (sys.argv[2], "w") as f:
        f.write(str(efficient_val) + "\n")
        f.write(efficient_string_1 + "\n")
        f.write(efficient_string_2 + "\n")
        f.write(str(time_taken) + "\n")
        f.write(str(memory_consumed))

if __name__ == "__main__":
    efficientDPApproach ()
