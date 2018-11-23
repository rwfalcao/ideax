//sort dashboard

$('a#dashboardSort').click(function () {

     var $divs = $(".profile-info");
     if(this.name == 'thumbsUp'){
         var mostLikesOrderedDivs = $divs.sort(function (a, b) {
             return $(a).data('like') < $(b).data('like');
         });
         $("#innovator-container").html(mostLikesOrderedDivs);
         $(".profile-info").wrapAll($("<div class='row mt-4'></div>"));
    }
     else if(this.name == 'thumbsDown'){
         var mostDislikesOrderedDivs = $divs.sort(function (a, b) {
             return $(a).data('dislike') > $(b).data('dislike');
         });
         $("#innovator-container").html(mostDislikesOrderedDivs);
         $(".profile-info").wrapAll($("<div class='row mt-4'></div>"));
    }

      else if(this.name == 'mostIdeas'){
          var maisIdeasOrderedDivs = $divs.sort(function (a, b) {
              return $(a).find('.qtdIdeas').text() < $(b).find('.qtdIdeas').text()
          });
          $("#innovator-container").html(maisIdeasOrderedDivs);
          $(".profile-info").wrapAll($("<div class='row mt-4'></div>"));
     }

     else if(this.name == 'fewerIdeas'){
         var menosIdeasOrderedDivs = $divs.sort(function (a, b) {
             return $(a).find('.qtdIdeas').text() > $(b).find('.qtdIdeas').text()
         });
         $("#innovator-container").html(menosIdeasOrderedDivs);
         $(".profile-info").wrapAll($("<div class='row mt-4'></div>"));
    }

     $('#dropdownMenuButton span.option').text($(this).text());
});
