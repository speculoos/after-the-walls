/*
 * 
 * ATW.views.js
 * 
 */

(function(undefined){
    'strict';
    var ATW = window.ATW;
    
    ATW.LogWidget = Backbone.View.extend({
        className:'log-widget widget',
        initialize:function(isLogged){
            this.isLogged = isLogged;
        },
        render:function(){
            var $el = this.$el;
            $el.empty();
            var data = {logged:this.isLogged};
            Template.render('log-widget', this, function(t){
                $el.html(t(data));
            });
            return this;
        },
        open:function(){
            
        },
        close:function(){
            
        },
        login:function(){
            
        },
        logout:function(){
            
        },
    });
    
    ATW.ContactWidget = Backbone.View.extend({
        className:'contact-widget widget',
        initialize:function(isLogged){
            this.isLogged = isLogged;
        },
        render:function(){
            var $el = this.$el;
            $el.empty();
            var data = {logged:this.isLogged};
            Template.render('contact-widget', this, function(t){
                $el.html(t(data));
            });
            return this;
        },
        open:function(){
            
        },
        close:function(){
            
        },
        send:function(){
            
        },
    });
    
    ATW.RegisterWidget = Backbone.View.extend({
        className:'register-widget widget',
        initialize:function(isLogged){
            this.isLogged = isLogged;
        },
        render:function(){
            var $el = this.$el;
            $el.empty();
            var data = {logged:this.isLogged};
            Template.render('register-widget', this, function(t){
                $el.html(t(data));
            });
            return this;
        },
        open:function(){
            
        },
        close:function(){
            
        },
        send:function(){
            
        },
    });
    
    ATW.VideoPlayer = Backbone.View.extend({
        className:'video-player',
        initialize:function(){
            
        },
        render:function(){
            var $el = this.$el;
            $el.empty();
            Template.render('video-player', this, function(t){
                $el.html(t(data));
            });
            return this;
        },
        play:function(){
            
        },
        pause:function(){
            
        },
        playHead:function(){
            
        },
        louder:function(){
            
        },
        softer:function(){
            
        },
        mute:function(){
            
        },
    });
})();
