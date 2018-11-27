//sort dashboard

$('a#dashboardSort').click(function () {

     var $divs = $(".innovator-info");
     if(this.name == 'thumbsUp'){
         var mostLikesOrderedDivs = $divs.sort(function (a, b) {
             return $(a).data('like') < $(b).data('like');
         });
         $("#innovator-container").html(mostLikesOrderedDivs);
         $(".innovator-info").wrapAll($("<div class='row mt-4'></div>"));
    }
     else if(this.name == 'thumbsDown'){
         var mostDislikesOrderedDivs = $divs.sort(function (a, b) {
             return $(a).data('dislike') < $(b).data('dislike');
         });
         $("#innovator-container").html(mostDislikesOrderedDivs);
         $(".innovator-info").wrapAll($("<div class='row mt-4'></div>"));
    }

      else if(this.name == 'collaborators'){
          var maisIdeasOrderedDivs = $divs.sort(function (a, b) {
              return $(a).find('.qtdIdeas').text() < $(b).find('.qtdIdeas').text()
          });
          $("#innovator-container").html(maisIdeasOrderedDivs);
          $(".innovator-info").wrapAll($("<div class='row mt-4'></div>"));
     }

     $('#dropdownMenuButton span.option').text($(this).text());
});
