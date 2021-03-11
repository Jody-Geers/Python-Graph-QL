/**
 * API Interaction
 * @param {obj} req - requested entity database interaction
 * @return {arr} data - result
 */
persistServer = req => {

    return new Promise( ( resolve, reject ) => {

        $.ajax({
            cache : false,
            crossDomain : true,
            timeout : 15000, // 0 = never say never
            xhrFields : {
                withCredentials : false
            },
            contentType: 'text/plain; charset=utf-8',
            method : 'POST',
            url : 'http://localhost:8080/api/' + req.type + '/',
            data: JSON.stringify( req )
        })
        .done( res => {

            resolve( res );

        })
        .fail( err => {

            reject( err );

        });

    });

};