var name, primaryEmail;

var helper = (function() {
  var BASE_API_PATH = 'plus/v1/';
  return {
    onSignInCallback: function(authResult) {
      gapi.client.load('plus','v1').then(function() {
        if (authResult['access_token']) {
          $.when($(".card-title").hide().text("Are you sure?")).then(function() {
            $(".card-title, #disconnect").show();
          });
        } else if (authResult['error']) {
          $.when($(".card-title").hide().text("No session found.")).then(function() {
            $(".card-title, #return").show();
          });
        }
      });
    },

    disconnect: function() {
      // Revoke the access token.
      $.ajax({
        type: 'GET',
        url: 'https://accounts.google.com/o/oauth2/revoke?token=' + gapi.auth.getToken().access_token,
        async: false,
        contentType: 'application/json',
        dataType: 'jsonp',
        success: function(result) {
          $("#disconnect").hide();
          $.when($(".card-title").hide().text("See you later!")).then(function() {
            $(".card-title, #return").show();
          });
        }
      });
    }
  };
})();

function onSignInCallback(authResult) {
  helper.onSignInCallback(authResult);
}