
f = function (t) {
    if (delete o.a.defaults.headers.csrf,
    "/api/www" === t.url.substring(0, 8)) {
        var e = Object(h.b)("kw_token");
        o.a.defaults.headers.csrf = e
    }
    var n = c()();
    return t.data || (t.data = {}),
        "get" === t.method ? (t.data.httpsStatus = 1,
            t.data.reqId = n,
            t.params = t.data || {},
            delete t.data) : t.url = t.url + "?reqId=".concat(n, "&httpsStatus=1"),
        new Promise((function (e, n) {
                o()(t).then((function (r) {
                        if (t.ignore)
                            e(r);
                        else {
                            var code = r.data.code;
                            200 == code ? e(r) : n(-1 == code ? {
                                status: 500
                            } : {
                                status: 404
                            })
                        }
                    }
                )).catch((function (e) {
                        if (e.message && e.message.includes("timeout") || !e.response)
                            n({
                                status: 502
                            });
                        else {
                            if (!t.ignore) {
                                var r = e.response.status;
                                n({
                                    status: r
                                })
                            }
                            n(e.response)
                        }
                    }
                ))
            }
        ))
}