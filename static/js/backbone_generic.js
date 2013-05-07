/*
 * ATW.backbone_generic.js
 * 
 */

(function(undefined){
    ATW.Modeler = function(callback, object){
        ATW.Models = {};
        ATW.Collections = {};
        ATW.Views = {};
        $.getJSON(ATW.Config.API_URL, function(data){
            _.each(data, function(mdata, model)
            {
                ATW.Models[model] = Backbone.Model.extend({
                    urlRoot: data[model].list_endpoint,
                    idAttribute: 'id',
                    initialize: function() { },
                    url: function() {
                        var temp_url = Backbone.Model.prototype.url.call(this);
                        return (temp_url.charAt(temp_url.length - 1) == '/' ? temp_url : temp_url+'/');
                    }
                });
                
                ATW.Collections[model] = Backbone.Collection.extend({
                    url: data[model].list_endpoint,
                    model: ATW.Models[model],
                    parse: function(response) {
                        this.meta = response.meta || {};
                        return response.objects || response;
                    }
                });
                
                ATW.Views[model] = Backbone.View.extend({
                    className: model,
                    initialize: function() {
                        this.model.on('change', this.render, this);
                        if(!this.model.isNew())
                        {
                            this.render();
                        }
                    },
                    render: function() {
                        var $el = this.$el;
                        $el.attr('id', model + '_' + this.model.id)
                        $el.empty();
                        var data = this.model.toJSON();
                        Template.render(model, this, function(t){
                            $el.html(t(data));
                            if(this.postRender)
                            {
                                this.postRender(data);
                            }
                        });
                        return this;
                    },
                });
            });
            
            if(callback && (typeof callback === 'function'))
            {
                var obj = object || window;
                callback.apply(obj, []);
            }
            
        });
    }
})();
