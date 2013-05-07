/*
 * 
 * ATW.app.js
 * 
 */


(function(undefined){
    'strict';
    
    var ImageProto = {
        events:{
            'click .previous':'previous',
            'click .next':'next',
        },
        previous:function(evt){
            this.trigger('previous');
        },
        next:function(evt){
            this.trigger('next');
        },
    };
    
    var EpisodeProto = {
        events:{
            'click .title':'play',
        },
        play:function(){
            window.router.navigate('episode/'+this.model.id, {trigger: true});
        },
    };
    
    var HomeView =  Backbone.View.extend({
        id:'galery',
        initialize:function(){
            this.images = new window.ATW.Collections.homeimage;
            this.images.on('add', this.renderOne, this);
            this.images.on('reset', this.render, this);
        },
        initBack:function(item){
            this.$el.backstretch(item.get('image'), {fade:'slow'});
            this.backstretch = this.$el.data('backstretch');
        },
        renderOne:function(item){
//             var i = new window.ATW.Views.homeimage({model:item});
//             this.$el.append(i.render().el);
            if(this.backstretch === undefined)
                this.initBack(item);
            else
                this.backstretch.images.push(item.get('image'));
            return this;
        },
        render:function(){
            this.images.each(function(item){
                this.renderOne(item);
            }, this);
            return this;
        },
        next:function(){
            
        },
    });
    
    var EpisodeCollectionView = Backbone.View.extend({
        id:'episodes',
        initialize:function(){
            this.episodes = new window.ATW.Collections.episode;
            this.episodes.on('add', this.renderOne, this);
            this.episodes.on('reset', this.render, this);
        },
        renderOne:function(item){
            var i = new window.ATW.Views.episode({model:item});
            this.$el.append(i.render().el);
            return this;
        },
        render:function(){
            this.episodes.each(function(item){
                this.renderOne(item);
            }, this);
            return this;
        },
    });
    
    
    
    var AppView =  Backbone.View.extend({
        el:'body',
        initialize:function(){
            this.components = {};
            window.ATW.Modeler(function(){
                _.extend(window.ATW.Views.homeimage.prototype, ImageProto);
                _.extend(window.ATW.Views.episode.prototype, EpisodeProto);
                
                this.medias = new ATW.Collections.media;
                this.medias.fetch();
                
                this.components.home = {
                    view: new HomeView,
                    visible: false,
                    rendered: false,
                };
                this.components.episodes = {
                    view:new EpisodeCollectionView,
                    visible:false,
                    rendered: false,
                };
                this.components.login = {
                    view:new ATW.LogWidget,
                    visible:false,
                    rendered: false,
                };
                this.components.register = {
                    view:new ATW.RegisterWidget,
                    visible:false,
                    rendered: false,
                };
                this.components.player = {
                    view:new ATW.VideoPlayer,
                    visible:false,
                    rendered: false,
                };
                this.components.home.view.images.fetch();
                this.components.episodes.view.episodes.fetch();
                this.episodes = this.components.episodes.view.episodes;
                
                
                this.trigger('ready');
            }, this);
        },
        render:function(){
            for(var k in this.components){
                var c = this.components[k];
                if(c.visible)
                {
                    this.$el.append(c.view.el);
                    if(!c.rendered)
                    {
                        c.view.render();
                        c.rendered = true;
                    }
                }
            }
        },
        setComponents:function(comps){
            for(var k in this.components){
                var c = this.components[k];
                c.visible = false;
                c.view.$el.detach();
            }
            for(var i=0; i<comps.length; i++)
            {
                var c = comps[i];
                try{
                    this.components[c].visible = true;
                }
                catch(e){
                    console.log('Could not activate: '+c);
                }
            }
            this.render();
        },
        playEpisode:function(id){
            var item = this.episodes.get(id);
            var medias = item.get('medias');
            var media = this.medias.findWhere({resource_uri:medias[0]})
            this.components.player.view.loadMedia(media);
        }
    });
    
    window.ATW.AppView =  AppView;
})();


