/*
 * 
 * ATW.app.js
 * 
 */


(function(undefined){
    var Router =  Backbone.Router.extend({
        routes:{
            'home': 'home',
            'episode/:id': 'episode'
        },
        home:function(){
            
        },
        episode:function(id){
            
        },
    });
    
    ATW.router = new Router;
})();


