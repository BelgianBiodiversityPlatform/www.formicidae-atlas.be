// We avoid polluting the global namespace:
// http://marcofranssen.azurewebsites.net/writing-modular-javascript-without-polluting-the-global-namespace/

; (function($, formidabel, window, document, undefined) {
	// Atlas follows the Module pattern
    var atlas = formidabel.atlas = formidabel.atlas || (function(){
        var privateVar = [];
        
        var Occurrence = Backbone.Model.extend({
            addToMap: function(){
                console.log("Ajout occurrence");
            }
        });

        var OccurrenceList = Backbone.Collection.extend({
			model: Occurrence,

            // Store the species_id, so it will be available to build retrieval URL
            initialize: function(species_id){
                this.species_id = species_id;
            },

            url: function(){
                return '/api/v1/species/' + this.species_id;
            },

            // The server "to be stored" data is returned in the occurrences attribute
            // That's what we should use to build each Occurrence
            parse: function(response){
                return response.occurrences;
            }
        });
        
        var OccurrenceSearch = Backbone.Model.extend({
            // Fill the data from server
            // Should we overrive fetch instead ?
            loadOccurrences: function(){
                col = new OccurrenceList(this.get('species_id'));
                this.set('collection', col); // We'll now have a collection attribute
                
                var that = this;
                col.fetch({success: function(){
                    // Once its loaded, render that !
                    v = new OccurrenceSearchView({model: that});
                    v.render();
                }});
            }
        });

        // Should receive a OccurrenceSearch as model argument
        var OccurrenceSearchView = Backbone.View.extend({
            el: $('#search_list'), // TODO: decouple

            render: function(){
                var m = this.model;

                // Add to search list
                $(this.el).append('<p>Recherche species ' + m.get('species_id') + '</p>');
                // Ask each occurrence to render itself
                m.get('collection').each(function(occ){
                    occ.addToMap();
                });

            }
        });

        var SearchView = Backbone.View.extend({
            events: {
                'submit #search': 'trigger_search'
            },

            trigger_search: function(){
                var s = new OccurrenceSearch({
                    species_id: this.$('#species_id').val(),
                    color: '#ab13cc' // Make color configurable
                });

                s.loadOccurrences();

                return false; // Don't submit the search form
            }
        });

        var bootstrap = function(app_container){
            // Main view that observes the search form
            var f = new SearchView({el: app_container});

        };

        // Export public members
        return {
			bootstrap: bootstrap
        };

    }());
}(jQuery, window._formidabel = window._formidabel || {}, window, document));