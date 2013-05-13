/*
 * 
 * ATW.router.js
 * 
 */


(function(undefined){
    var Router =  Backbone.Router.extend({
        navigate:function(route, options){
            options = _.extend({trigger: true}, options);
            Backbone.Router.prototype.navigate.apply(this, [route, options]);
        },
        routes:{
            '': 'home',
            'visit': 'visit',
            'episode/:id': 'episode',
            'register': 'register',
            'profile' : 'profile',
            'logout': 'logout',
            'setlang/:code':'setlang',
        },
        home:function(){
            if(!app.isLogged())
            {
                app.setComponents('home audio register visit login'.split(' '));
                app.playAudio('/static/home.m4a');
            }
            else
                this.visit();
        },
        visit:function(){
            app.setComponents('player login'.split(' '));
            app.playDefault();
        },
        episode:function(id){
            app.setComponents('player login'.split(' '));
            app.playEpisode(id);
        },
        register:function(){
            app.setComponents('home register'.split(' '));
        },
        profile:function(){
            app.setComponents('profile'.split(' '));
        },
        logout:function(){
            $.ajax({
                type: "GET",
                url: '/logout',
                data: {  },
                dataType: 'json'
            });
            ATW.Config.user_name = undefined;
            ATW.Config.api_key = undefined;
            app.resetViews(['login','contact']);
            this.navigate('visit');
        },
        setlang:function(code){
            var self = this;
            $.ajax({
                type: "POST",
                url: '/i18n/setlang/',
                data: { language:code },
//                    dataType: 'json'
            });
            var href = window.location.href;
            var baseloc= href.protocol + '//'+ href.host
            href = baseloc;
        },
    });
    
    ATW.Router = Router;
})();


