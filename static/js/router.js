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
        },
        home:function(){
            if(!app.isLogged())
                app.setComponents('home register visit login'.split(' '));
            else
                this.visit();
        },
        visit:function(){
            app.setComponents('episodes player login contact'.split(' '));
            app.playDefault();
        },
        episode:function(id){
            app.setComponents('episodes player login contact'.split(' '));
            app.playEpisode(id);
        },
        register:function(){
            app.setComponents('home register'.split(' '));
        },
    });
    
    ATW.Router = Router;
})();


