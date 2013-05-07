/*
 * 
 * ATW.router.js
 * 
 */


(function(undefined){
    var Router =  Backbone.Router.extend({
        routes:{
            '': 'home',
            'episode/:id': 'episode',
            'register': 'register',
            'contact': 'contact',
        },
        home:function(){
            console.log('home');
            app.setComponents('home login register contact'.split(' '));
        },
        episode:function(id){
            console.log('episode: '+id);
            app.setComponents('episodes login register contact'.split(' '));
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


