/*
 * 
 * ATW.router.js
 * 
 */


(function(undefined){
    var Router =  Backbone.Router.extend({
        routes:{
            '': 'home',
            'visit': 'visit',
            'episode/:id': 'episode',
            'register': 'register',
            'contact': 'contact',
        },
        home:function(){
            console.log('home');
            if(ATW.Config.user_name === undefined)
                app.setComponents('home login contact'.split(' '));
            else
                this.visit();
        },
        visit:function(){
            console.log('visit');
            app.setComponents('episodes player login contact'.split(' '));
        },
        episode:function(id){
            console.log('episode: '+id);
            app.setComponents('episodes player login contact'.split(' '));
            app.playEpisode(id);
        },
//         register:function(){
//             console.log('register');
//         },
//         contact:function(){
//             console.log('contact');
//         },
    });
    
    ATW.Router = Router;
})();


