var name, primaryEmail;

var helper = (function() {
  var BASE_API_PATH = 'plus/v1/';
  return {
    onSignInCallback: function(authResult) {
      gapi.client.load('plus','v1').then(function() {
        if (authResult['access_token']) {
          $('#content').fadeOut('slow', function() {
            $('.g-signin').hide();
            $('#welcome').empty();
            helper.profile();
            $('#content').fadeIn('slow');
          });
        } else if (authResult['error']) {
          $('#button.g-signin').show();
        }
      });
    },

    profile: function(){
      gapi.client.plus.people.get({
        'userId': 'me'
      }).then(function(res) {              
        var profile = res.result;
        name = profile.displayName;
        $('#welcome').text("Welcome back, " + name.split(" ")[0] + "!");

        for (var i=0; i < profile.emails.length; i++) {
          if (profile.emails[i].type === 'account') primaryEmail = profile.emails[i].value;
        }

        $("#content").css('margin-top', (-1 * $("#content").height()/2 - 84) + 'px');
        $('#spinner').delay(1000).fadeIn('slow');
      }, function(err) {
        var error = err.result;
        $('#error').append(error.message);
      }).then(function() {
        function authenticate() {
          helper.authenticate(primaryEmail, name);
        }
        window.setTimeout( authenticate, 5000 );
      });
    },

    authenticate: function(email, name) {
      $.ajax({
        url: "/authenticate",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify  ({
          "email": email,
          "name": name
        }),
        success: function(result) {
          window.location.replace(result);
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
          location.reload();
        }
      });
    }
  };
})();

function onSignInCallback(authResult) {
  helper.onSignInCallback(authResult);
}