"use strict";
var fs = require("fs");
var bookList = ["a game of thrones", "a clash of kings", "a storm of swords", "a feast for crows", "a dance with dragons"];

fs.readFile("wiki_characters.txt", "utf8", function(err, text) {
  var lines = text.split("\n");
  var chars = lines.map(function(line) {
    var char = {};
    var data = line.split("^");
    char.name = data[0];
    char.allegiances = data[1];
    var deathDate = data[2];
    var deathDataRe = data[2] ? data[2].match(/[0-9]+/) : null;
    char.dead = deathDataRe ? deathDataRe[0] : "";
    var books = data[3] ? data[3].split(",") : [];
    var bookCount = 0;
    char.actualBooks = [0,0,0,0,0];
    for (var i = 0; i < books.length; i++) {
      var book = books[i].trim().toLowerCase();
      var appearsLoc = book.indexOf(" (appears");
      var povLoc = book.indexOf(" (pov");
      var mentionedLoc = book.indexOf(" (mentioned");
      if (appearsLoc != -1 || povLoc != -1) {
        var marker = appearsLoc > povLoc ? appearsLoc : povLoc;
        book = book.slice(0, marker);
        var seriesBookIndex = bookList.indexOf(book);
        if (seriesBookIndex != -1) {
          bookCount++;
          char.actualBooks[seriesBookIndex] = 1;
        }
      } else if (mentionedLoc === -1) {
        var seriesBookIndex = bookList.indexOf(book);
        if (seriesBookIndex != -1) {
          bookCount++;
          char.actualBooks[seriesBookIndex] = 1;
        }
      }
    }
    char.csvString = char.name+","+char.allegiances+","+char.dead+","+char.actualBooks+"\n";
    if (bookCount > 0) {
      fs.appendFile("parsed_characters.txt", char.csvString);
    }
    return char;
  });
  
});