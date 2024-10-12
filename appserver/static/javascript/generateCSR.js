require([
    "jquery",
    "splunkjs/mvc/searchmanager",
    "splunkjs/mvc/simplexml/ready!"
], function(
    $,
    SearchManager
) {
    function getInputValues() {
        var sanInputs = $('.san_input').map(function() {
            return $(this).val().trim();
        }).get();

        return {
            cn: $('#cn_input').val().trim(),
            country: $('#country_input').val().trim(),
            state: $('#state_input').val().trim(),
            locality: $('#locality_input').val().trim(),
            organization: $('#organization_input').val().trim(),
            organizationalunit: $('#organizationalunit_input').val().trim(),
            subjectAltNames: sanInputs.filter(Boolean).join(',')
        };
    }

    function validateInputs(inputs) {
        var errors = [];
        
        if (!inputs.cn) {
            errors.push("Common Name (CN) cannot be empty.");
        } else if (!/^[a-zA-Z0-9.-]+$/.test(inputs.cn)) {
            errors.push("Common Name (CN) must be a valid domain name (letters, numbers, dots, dashes only).");
        }

        if (inputs.subjectAltNames.length > 0) {
            var sanArray = inputs.subjectAltNames.split(',');
            sanArray.forEach(function(san) {
                if (!/^[a-zA-Z0-9.-]+$/.test(san.trim())) {
                    errors.push("Each Subject Alternative Name must be a valid domain name (letters, numbers, dots, dashes only).");
                }
            });
        }

        return errors;
    }

    $(".button1").on("click", function() {
        var ok = confirm("Are you sure you want to generate a .key file and a .csr file with these parameters?");
        if (ok) {
            var inputValues = getInputValues();
            var validationErrors = validateInputs(inputValues);

            if (validationErrors.length > 0) {
                alert("Please fix the following errors:\n" + validationErrors.join("\n"));
                return;
            }

            var gen_key_csr = new SearchManager({
                id: "gen_key_csr",
                autostart: false,
                search: '| gencsr common_name="' + inputValues.cn + 
                        '" country="' + inputValues.country + 
                        '" state="' + inputValues.state + 
                        '" locality="' + inputValues.locality + 
                        '" organization="' + inputValues.organization + 
                        '" organizationalunit="' + inputValues.organizationalunit + 
                        '" subjectaltname="' + inputValues.subjectAltNames + '"'
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
                    } else {
                        $('.success').hide();
                    }
                });
            });

            gen_key_csr.startSearch();
        }
    });

    $('#add_san').on("click", function() {
        $('#san_container').append('<input type="text" class="san_input" placeholder="e.g., sanN.example.com"/>');
    });
});
