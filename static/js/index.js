/*
 * index.js
 */

$(document).ready(function(){
    var app = window.app = new window.ATW.AppView;
    
    app.on('ready', function(){
        console.log('Application Ready');
        window.router = new ATW.Router;
        Backbone.history.start({pushState: false});
        $('body').on('click', '.link', function(evt){
            var that = $(this);
            that.addClass('visited');
            window.router.navigate(that.attr('data-src'));
        });
    });
});
