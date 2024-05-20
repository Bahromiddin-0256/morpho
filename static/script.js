document.getElementById('analyzeForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const inputText = document.getElementById('inputText').value;

    fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `input_text=${encodeURIComponent(inputText)}`
    })
    .then(response => response.json())
    .then(data => {
        const resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = '';

        for (const [word, analysis] of Object.entries(data)) {
            const resultItem = document.createElement('div');
            resultItem.classList.add('result-item');
            resultItem.innerHTML = `<strong>${word}:</strong> ${analysis.join(', ')}`;
            resultsDiv.appendChild(resultItem);
        }
    });
});
