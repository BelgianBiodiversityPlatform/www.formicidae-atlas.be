// We avoid polluting the global namespace:
// http://marcofranssen.azurewebsites.net/writing-modular-javascript-without-polluting-the-global-namespace/

; (function($, formidabel, window, document, undefined) {
	// Atlas follows the Module pattern
    var atlas = formidabel.atlas = formidabel.atlas || (function(){
        var privateVar = [];
        
        var Occurrence = Backbone.Model.extend({});
        var OccurrenceList = Backbone.Collection.extend({
			model: Occurrence,

            initialize: function(species_id){
                this.species_id = species_id;
            },

            url: function(){
                return '/api/v1/species/' + this.species_id;
            }
        });
        
        var OccurrenceSearch = Backbone.Model.extend({
            // Fill the data from server
            // Should we overrive fetch instead ?
            loadOccurrences: function(){
                var col = new OccurrenceList(this.get('species_id'));

                this.set({occurrences: col.fetch()});
            }
        });

        var bootstrap = function(){
			var s = new OccurrenceSearch({species_id: 372, color: '#ab13cc'});
            s.loadOccurrences();
        };

        // Export public members
        return {
			bootstrap: bootstrap
        };

    }());
}(jQuery, window._formidabel = window._formidabel || {}, window, document));