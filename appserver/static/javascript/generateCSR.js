require([
    "jquery",
    "splunkjs/mvc/searchmanager",
    "splunkjs/mvc/simplexml/ready!"
], function(
    $,
    SearchManager
) {
    function getInputValues() {
        return {
            cn: $('#cn_input').val(),
            country: $('#country_input').val(),
            state: $('#state_input').val(),
            locality: $('#locality_input').val(),
            organization: $('#organization_input').val(),
            organizationalunit: $('#organizationalunit_input').val()
        };
    }
    $(".button1").on("click", function() {
        var ok = confirm("Are you sure you want to generate a .key file and a .csr file with these parameters?");
        if (ok) {
            var inputValues = getInputValues();
            var gen_key_csr = new SearchManager({
                id: "gen_key_csr",
                autostart: false,
                search: '| gencsr common_name="' + inputValues.cn + '" country="' + inputValues.country + '" state="' + inputValues.state + '" locality="' + inputValues.locality + '" organization="' + inputValues.organization + '" organizationalunit="' + inputValues.organizationalunit + '"'
            });
            gen_key_csr.on('search:done', function() {
                gen_key_csr.data('results', {count: 1}).on('data', function(results) {
                    if (results.hasData()) {
                    
                        var csr = results.data().rows[0][2];
                        var key = results.data().rows[0][3]; 

                        $('#csr_output').text(csr);
                        $('#key_output').text(key);
                        $('.success').show();
                        $('.results').show();
                    }
                });
            });
            gen_key_csr.startSearch();
        }
    });
});
