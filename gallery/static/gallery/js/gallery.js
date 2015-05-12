var request = new XMLHttpRequest();
request.open("get", "/json/");
request.send(null);
request.addEventListener("load", function (response) {
    var data = JSON.parse(request.responseText);
    React.render(
	React.createElement(
	    "div",
	    null,
	    _.map(data.repos, function (repo) {
		return React.createElement(
		    "div",
		    null,
		    [
			React.createElement(
			    "div",
			    {
				className: "col-xs-12 col-sm-12 col-md-6 col-lg-6",
				key: repo.id,
				style: {textAlign: "center"}
			    },
			    [
				React.createElement(
				    "div",
				    {className: "col-xs-6 col-sm-6 col-md-6 col-lg-6"},
				    React.createElement("img", {className: "img-responsive img-circle", src: "/static/gallery/png/bomberman.png", style: {maxWidth: "100%"}})
				),
				React.createElement(
				    "div",
				    {className: "col-xs-6 col-sm-6 col-md-6 col-lg-6"},
				    React.createElement("h2", null, repo.name)
				),
				React.createElement(
				    "div",
				    {className: "col-xs-12 col-sm-12 col-md-12 col-lg-12"},
				    _.map(data.contributers, function (contributor) {
					if (_.contains(contributor.repos, repo.id)) {
					    return React.createElement("div", {className: "row"}, [
						React.createElement(
						    "div",
						    {className: "col-xs-1 col-sm-1 col-md-1 col-lg-1"},
						    React.createElement("img", {src: "https://avatars.githubusercontent.com/u/632397?v=3", style: {maxWidth: "100%"}})
						),
						React.createElement(
						    "div",
						    {className: "col-xs-11 col-sm-11 col-md-11 col-lg-11"},
						    React.createElement("h6", null, contributor.name)
						)
					    ]);
					}
				    })
				)
			    ]
			),
			React.createElement(
			    "div",
			    {className: "col-xs-12 col-sm-12 col-md-6 col-lg-6", style: {textAlign: "center"}},
			    repo.description
			),
			React.createElement(
			    "div",
			    {style: {clear: "both"}}
			)
		    ]
		);
	    })
	),
	document.getElementById("root")
    );
});
