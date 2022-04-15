function loadStats(repoName) {
    let stats = fetch(`https://api.github.com/repos/${repoName}`)
        .then(result => result.json())
        .then(data => {
            document.getElementById("size").innerText = `${data.size} KB`;
            document.getElementById("stars").innerText = `${data.stargazers_count}`;
            document.getElementById("forks").innerText = `${data.forks_count}`;
            document.getElementById("watchers").innerText = `${data.watchers_count}`;
        })

    let commits = fetch(`https://api.github.com/repos/${repoName}/commits`)
        .then(result => result.json())
        .then(data => {
            document.getElementById("version").innerText = `${data.length}` 
        })
}