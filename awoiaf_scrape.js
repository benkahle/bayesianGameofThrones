"use strict";
var request = require("request");
var env = require("jsdom").env;
var fs = require("fs");

var rootUrl = "http://awoiaf.westeros.org";

request("http://awoiaf.westeros.org/index.php/List_of_characters", function (error, response, body) {
  if (!error && response.statusCode == 200) {
    env(body, function(errors, window) {
      var $ = require("jquery")(window);
      var tags = $("#bodyContent li>a:first-child");
      var characterLinks = tags.map(function(tagNum) {
        var relUrl = tags[tagNum].href;
        return rootUrl+relUrl.substring(7); //Chop off "file://"
      });
      for (var i = 0; i < characterLinks.length ; i++) {
        // fs.appendFile("wiki_links.txt", characterLinks[i]+"\n");
        request(characterLinks[i], function(err, resp, pageBody) {
          if (!err && resp.statusCode == 200) {
            env(pageBody, function (errors, window) {
              var $ = require("jquery")(window);
              var name = $("#firstHeading").text();
              var houses = $(".infobox th:contains('Allegiance')").siblings("td").children("a").map(function() { return $(this).text(); }).get().join(";");
              var died = $(".infobox th:contains('Died')").siblings("td").text();
              var books = $(".infobox th:contains('Book(s)')").siblings("td").text().split(')');
              var line = name+"^"+houses+"^"+died+"^"+books+"\n";
              fs.appendFile("wiki_characters.txt", line);
            });
          }
        });
      }
    });
  }
});