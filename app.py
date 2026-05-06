from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    score = None
    if request.method == 'POST':
        seq1 = request.form.get('seq1').strip().upper()
        seq2 = request.form.get('seq2').strip().upper()

        match_score = 1
        mismatch_score = -1
        gap_penalty = -1

        rows = len(seq1) + 1
        cols = len(seq2) + 1
        matrix = [[0 for _ in range(cols)] for _ in range(rows)]

        for i in range(rows):
            matrix[i][0] = i * gap_penalty
        for j in range(cols):
            matrix[0][j] = j * gap_penalty

        for i in range(1, rows):
            for j in range(1, cols):
                if seq1[i - 1] == seq2[j - 1]:
                    diagonal_score = matrix[i - 1][j - 1] + match_score
                else:
                    diagonal_score = matrix[i - 1][j - 1] + mismatch_score
                    
                up_score = matrix[i - 1][j] + gap_penalty
                left_score = matrix[i][j - 1] + gap_penalty

                matrix[i][j] = max(diagonal_score, up_score, left_score)

        score = matrix[-1][-1]

    return render_template('index.html', score=score)

if __name__ == '__main__':
    app.run(debug=True, port=5003)