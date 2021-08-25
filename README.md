# <p align="center">Fessor</p>

[![Version Badge](https://img.shields.io/github/v/tag/nangurepo/fessor?label=version)](https://img.shields.io/github/v/tag/nangurepo/fessor?label=version)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/97c57bb49e0f4fbe94b38967169f17c4)](https://app.codacy.com/gh/NanguRepo/fessor?utm_source=github.com&utm_medium=referral&utm_content=NanguRepo/fessor&utm_campaign=Badge_Grade_Settings)
[![License Badge](https://img.shields.io/github/license/nangurepo/fessor)](https://img.shields.io/github/license/nangurepo/fessor)
[![Build Badge](https://img.shields.io/github/workflow/status/nangurepo/fessor/Pylint)](https://img.shields.io/github/workflow/status/nangurepo/fessor/Pylint)
[![Checks Badge](https://img.shields.io/github/checks-status/nangurepo/fessor/main)](https://img.shields.io/github/checks-status/nangurepo/fessor/main)
[![Lines Badge](https://img.shields.io/tokei/lines/github/nangurepo/fessor)](https://img.shields.io/tokei/lines/github/nangurepo/fessor)
[![Redditor Badge](https://img.shields.io/reddit/user-karma/combined/nangu_?label=reddit%20karma)](https://reddit.com/u/nangu_)

<style>
    kbd {
    background-color: #eee;
    border-radius: 3px;
    border: 1px solid #b4b4b4;
    box-shadow: 0 1px 1px rgba(0, 0, 0, .2), 0 2px 0 0 rgba(255, 255, 255, .7) inset;
    color: #333;
    display: inline-block;
    font-size: .85em;
    font-weight: 700;
    line-height: 1;
    padding: 2px 4px;
    white-space: nowrap;
   }
   /* Style the button that is used to open and close the collapsible content */
    .collapsible {
    background-color: #eee;
    color: #444;
    cursor: pointer;
    padding: 18px;
    width: 100%;
    border: none;
    text-align: left;
    outline: none;
    font-size: 15px;
    }

    /* Add a background color to the button if it is clicked on (add the .active class with JS), and when you move the mouse over it (hover) */
    .active, .collapsible:hover {
    background-color: #ccc;
    }

    /* Style the collapsible content. Note: hidden by default */
    .content {
    padding: 0 18px;
    display: none;
    overflow: hidden;
    background-color: #f1f1f1;
    }
</style>

<button type="button" class="collapsible">Open Collapsible</button>
<div class="content">
  <p>Lorem ipsum...</p>
</div>

<script>
var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });
}
</script>

## Features
-   Viggo assignment scanner
-   Permission system
-   Moderation features
-   <kbd>/</kbd> Slash commands
-   Chat burying! - A great, new, non-destructive alternative to purging chat
