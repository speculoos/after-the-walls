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
        },
        home:function(){
            if(!app.isLogged())
                app.setComponents('home register visit login'.split(' '));
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
            ATW.Config.user_name = undefined;
            ATW.Config.api_key = undefined;
            app.resetViews(['login','contact']);
        },
    });
    
    ATW.Router = Router;
})();


