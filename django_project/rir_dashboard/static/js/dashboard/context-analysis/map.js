$(document).ready(function () {
    let map = L.map('map',).setView([5.2310274, 48.8058511], 5);
    const basemaps = {
        'OSM': L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            noWrap: true,
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map)
    }
    //
    const layerControl = L.control.layers(basemaps, []).addTo(map);

    map.on('overlayadd', e => $(`div[data-layer="${e.name}"]`).show());
    map.on('overlayremove', e => $(`div[data-layer="${e.name}"]`).hide());

    initLayer(map, layers, 0);


    /**
     * TODO:
     *  We need to move this to model
     */
    function initLayer(map, layers, idx) {
        const layer = layers[idx];
        if (layer) {
            const name = layer[0];
            const url = layer[1];
            const fieldName = layer[2];
            const params = layer[3];
            const options = layer[4];

            const layerType = layer[5];

            switch (layerType) {
                case 'ESRI':
                    (new EsriLeafletLayer(
                        map, name, url, fieldName, params, options
                    )).load().then(layer => {
                        if (layer) {
                            layerControl.addOverlay(layer, name);
                        }
                        initLayer(map, layers, idx + 1);
                    }).catch(e => {
                        initLayer(map, layers, idx + 1);
                    });
                    break;
                case 'Raster':
                    const layer = L.tileLayer.wms(url, params);
                    if (layer) {
                        layerControl.addOverlay(layer, name);
                    }
                    initLayer(map, layers, idx + 1);
                    break
                default:
                    initLayer(map, layers, idx + 1);

            }
        }
    }
});


// // INIT LAYER
const layers = [
    [
        'Troop Locations', 'https://services3.arcgis.com/7J7WB6yJX0pYke9q/arcgis/rest/services/som_troop_locations/FeatureServer/0', 'Group_',
        {},
        {
            token: '-7KzAsLHiJ0XWT4-Ujy8F4loC6sWrhm8_oxc2zBB7onazKaQv7SYOOHzcods_xAEMbToynDXh1UrkfQwT0Qh-V1AQpP0uxdwaKcWNOSs--38OpkbgxhvfNm9nH9eon3xFGgjIxOlBNxlIUyhNHKne59s7fBMN39DZHUJpjCscfvlHp7TnL7M5_N9e1gX-jBSBG2d8-JfVISPpT3QHVvCIYnPCmLoDv2g8CvotSYMZNV-nHRb4-lbODr_3Ri-OO4XJQxFJU5c58IPYQcHkSFj3n9680zm5RH7I2QpV6n3JDCBfK1PodAcAq_Q-wzfRwXW'
        },
        'ESRI'
    ],
    [
        'Covid 19', 'https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/1', 'Confirmed',
        {
            where: "Country_Region='Somalia'"
        },
        {},
        'ESRI'
    ],
    [
        'Locus Bands', 'https://services5.arcgis.com/sjP4Ugu5s0dZWLjd/ArcGIS/rest/services/Bands_Public/FeatureServer/0', '',
        {
            where: "COUNTRYID='SO'"
        },
        {},
        'ESRI'
    ],
    [
        'Locus Adult', 'https://services5.arcgis.com/sjP4Ugu5s0dZWLjd/ArcGIS/rest/services/Adults_Public/FeatureServer/0', '',
        {
            where: "COUNTRYID='SO'"
        },
        {},
        'ESRI'
    ],
    [
        'Locus Swarm', 'https://services5.arcgis.com/sjP4Ugu5s0dZWLjd/ArcGIS/rest/services/Swarms_Public/FeatureServer/0', '',
        {
            where: "COUNTRYID='SO'"
        },
        {},
        'ESRI'
    ],
    [
        'ACLED - Past Two Weeks', 'https://services.arcgis.com/LG9Yn2oFqZi5PnO5/arcgis/rest/services/Armed_Conflict_Location_Event_Data_ACLED/FeatureServer/0', 'event_type',
        {
            where: "country = 'Somalia'"
        },
        {},
        'ESRI'
    ],
    [
        'ACLED - Hotspots', 'https://services3.arcgis.com/7J7WB6yJX0pYke9q/arcgis/rest/services/SOM_ACLED_2020_2019_HotSpots/FeatureServer/0', 'Gi_Bin',
        {},
        {
            token: 'Vil5bGfrxH7P1SQPCrDWzqtnAXt_unnQ5y_uDeonPC1z3Kq5o0fcd_sMSNW4Dch3OsKA720UlXFyCtP7dcuKcrewAJ5A-lmATDKi3CjyD01Rr0KcNoJJAshrMsI-XxauyRsowC9uPv9DylJobcWKg0xbIJxoCit2ECEW81gNzlR5Fqp0gdS_CmXMXUIvkcRDVSVcRy1mLPEBdQgKV4dDpUvH342XzgmOcFVNfF6MLrMbJLt6HewcUe7Vcv0qCApDbLQUkjDXOra5I62b2m3eZAQ_ihSGgn_xkI2o-vxY_dAcqxvql7uzFmZtyq0gvZDX'
        },
        'ESRI'
    ],
    [
        'Refugees and IDPs', 'https://gis.unhcr.org/arcgis/rest/services/core/wrl_ppl_poc_p_unhcr/FeatureServer/0', 'loc_type',
        {
            where: "(iso3 = 'SOM') OR (iso3 = 'KEN') OR (iso3 = 'ETH') OR (iso3 = 'DJI')"
        },
        {},
        'ESRI'
    ],
    [
        'Access - Airport', 'https://services6.arcgis.com/iEFoPS2vWoeRJSAA/arcgis/rest/services/Airport/FeatureServer/0', '',
        {},
        {},
        'ESRI'
    ],
    [
        'Access - Ports', 'https://services6.arcgis.com/iEFoPS2vWoeRJSAA/arcgis/rest/services/Sea_Ports/FeatureServer/0', '',
        {},
        {},
        'ESRI'
    ],
    [
        'Access - Border Crossing', 'https://services6.arcgis.com/iEFoPS2vWoeRJSAA/arcgis/rest/services/Entry_points/FeatureServer/0', '',
        {},
        {},
        'ESRI'
    ],
    [
        'Control - Capitals', 'https://services3.arcgis.com/7J7WB6yJX0pYke9q/arcgis/rest/services/Somalia_Capitals_Control/FeatureServer/0', 'Control',
        {},
        {
            token: 'vRcLzfR7u4ToOHSzUoeyHnVCo6ZPaQSOvza3SFWmuGDQPUBNefTariqQJK6rYQDskGTZ6lVrwcboYUroreLFRUpVVhgkFOMJ38mRi0K5v9jRIjA-Rg0A-RosqvgpPe4aoWwsL461zMfccuEjr574aAnWbdBT6o-G7kiYGZxU7a1QDEnrLsPdcVjnFq4jCwQE0P0miGDnPHAc59uhML5v-igAchGZ2o9W_nv7exkHZPnxg-bpKPJ5ifK0uGQhigBBseGIZ5HYgL_HvV6FFf6YYnq30nxQTTD9dKL1_qhSxO45E1EKftXnquyJq0yOOd3S'
        },
        'ESRI'
    ],
    [
        'Control - Roads', 'https://services3.arcgis.com/7J7WB6yJX0pYke9q/arcgis/rest/services/Somalia_Roads_Control/FeatureServer/1', 'Control',
        {},
        {
            token: 'vRcLzfR7u4ToOHSzUoeyHnVCo6ZPaQSOvza3SFWmuGDQPUBNefTariqQJK6rYQDskGTZ6lVrwcboYUroreLFRUpVVhgkFOMJ38mRi0K5v9jRIjA-Rg0A-RosqvgpPe4aoWwsL461zMfccuEjr574aAnWbdBT6o-G7kiYGZxU7a1QDEnrLsPdcVjnFq4jCwQE0P0miGDnPHAc59uhML5v-igAchGZ2o9W_nv7exkHZPnxg-bpKPJ5ifK0uGQhigBBseGIZ5HYgL_HvV6FFf6YYnq30nxQTTD9dKL1_qhSxO45E1EKftXnquyJq0yOOd3S'
        },
        'ESRI'
    ],
    [
        'Control - District', 'https://services3.arcgis.com/7J7WB6yJX0pYke9q/arcgis/rest/services/Somalia_District_Control/FeatureServer/1', 'Control',
        {},
        {
            token: 'vRcLzfR7u4ToOHSzUoeyHnVCo6ZPaQSOvza3SFWmuGDQPUBNefTariqQJK6rYQDskGTZ6lVrwcboYUroreLFRUpVVhgkFOMJ38mRi0K5v9jRIjA-Rg0A-RosqvgpPe4aoWwsL461zMfccuEjr574aAnWbdBT6o-G7kiYGZxU7a1QDEnrLsPdcVjnFq4jCwQE0P0miGDnPHAc59uhML5v-igAchGZ2o9W_nv7exkHZPnxg-bpKPJ5ifK0uGQhigBBseGIZ5HYgL_HvV6FFf6YYnq30nxQTTD9dKL1_qhSxO45E1EKftXnquyJq0yOOd3S'
        },
        'ESRI'
    ],
    [
        'IPC project April June 2021', 'https://services3.arcgis.com/7J7WB6yJX0pYke9q/arcgis/rest/services/Somalia_Clan_Distribution/FeatureServer/0', "Gu_19",
        {},
        {
            token: 'vRcLzfR7u4ToOHSzUoeyHnVCo6ZPaQSOvza3SFWmuGDQPUBNefTariqQJK6rYQDskGTZ6lVrwcboYUroreLFRUpVVhgkFOMJ38mRi0K5v9jRIjA-Rg0A-RosqvgpPe4aoWwsL461zMfccuEjr574aAnWbdBT6o-G7kiYGZxU7a1QDEnrLsPdcVjnFq4jCwQE0P0miGDnPHAc59uhML5v-igAchGZ2o9W_nv7exkHZPnxg-bpKPJ5ifK0uGQhigBBseGIZ5HYgL_HvV6FFf6YYnq30nxQTTD9dKL1_qhSxO45E1EKftXnquyJq0yOOd3S'
        },
        'ESRI'
    ],
    [
        'Clan Distribution', 'https://services3.arcgis.com/7J7WB6yJX0pYke9q/arcgis/rest/services/Somalia_Clan_Distribution/FeatureServer/0', "CLAN_FAM",
        {},
        {
            token: '40lRfiYaUUIYpbcErr2bvch2TCPYQ8HO6PvFUECrZqzRRr1hMvlgtpwV-rNtFnE7HpjwgfK54Ue-5QKvOZF5axVgK2hInLuadFuqrIxfg3_Mz5osDzCwrfhi0d7xJ9_dqPHhpX2h9V5ytwXiJHDx9T11hcG9QeR7WD_n2rcvjKu2cpHsFqRRh4PFioU7Q5edeQAJ5HGxG_OSHL745pk-dEOcRPx70PvIxULuui5x-Dueanmalc03SJ5fCWhpiJytOAz2tbPQq1RdeFtzf41-alb3CqWSZjK1tCu3aLgcj-3scbO4LvP1SJNcnv2Nd265'
        },
        'ESRI'
    ],
    [
        'Program Coverage', 'https://services3.arcgis.com/7J7WB6yJX0pYke9q/arcgis/rest/services/Somalia_District_ProgCoverage/FeatureServer/0', "",
        {},
        {
            token: '40lRfiYaUUIYpbcErr2bvch2TCPYQ8HO6PvFUECrZqzRRr1hMvlgtpwV-rNtFnE7HpjwgfK54Ue-5QKvOZF5axVgK2hInLuadFuqrIxfg3_Mz5osDzCwrfhi0d7xJ9_dqPHhpX2h9V5ytwXiJHDx9T11hcG9QeR7WD_n2rcvjKu2cpHsFqRRh4PFioU7Q5edeQAJ5HGxG_OSHL745pk-dEOcRPx70PvIxULuui5x-Dueanmalc03SJ5fCWhpiJytOAz2tbPQq1RdeFtzf41-alb3CqWSZjK1tCu3aLgcj-3scbO4LvP1SJNcnv2Nd265'
        },
        'ESRI'
    ],
    [
        'Monitoring_WASH_20201116', 'https://services3.arcgis.com/7J7WB6yJX0pYke9q/arcgis/rest/services/Monitoring_WASH_20201116/FeatureServer/0', "",
        {},
        {
            token: '9LkHUtPISDQr5aRJTTPXE-zbIWVgkCSqn10q5Xpo_xYc8XDdSijqImR4RbCeGxLlCl6n-UlwOwhnC3KZIqTF2guYdmMySyHzEUFRPFdPgEHK7pl813wBSoAbY8mQBOHE-8iCRvv06i-DfNnJ8Olm6ONOmaF3ms-j1UwZGmw4owDTI6ZDjwFKW0-iEo_vfPau2E_j0LNf0u1t0sZ9cxNL5Z69XLhvPa0UbgA0Ogdh4f-MREFCWg1glT3xpZYu4GC0CeFXDS6hH0zLunkmjUYHmUIv7ttJJCgSMwMaum9P8Tv9hgyXWucysJkNbuLbjr7P'
        },
        'ESRI'
    ],
    [
        'Monitoring_Nutrition_20201116', 'https://services3.arcgis.com/7J7WB6yJX0pYke9q/arcgis/rest/services/Monitoring_Nutrition_20201116/FeatureServer/0', "",
        {},
        {
            token: '9LkHUtPISDQr5aRJTTPXE-zbIWVgkCSqn10q5Xpo_xYc8XDdSijqImR4RbCeGxLlCl6n-UlwOwhnC3KZIqTF2guYdmMySyHzEUFRPFdPgEHK7pl813wBSoAbY8mQBOHE-8iCRvv06i-DfNnJ8Olm6ONOmaF3ms-j1UwZGmw4owDTI6ZDjwFKW0-iEo_vfPau2E_j0LNf0u1t0sZ9cxNL5Z69XLhvPa0UbgA0Ogdh4f-MREFCWg1glT3xpZYu4GC0CeFXDS6hH0zLunkmjUYHmUIv7ttJJCgSMwMaum9P8Tv9hgyXWucysJkNbuLbjr7P'
        },
        'ESRI'
    ],
    [
        'Monitoring_Health_20201116', 'https://services3.arcgis.com/7J7WB6yJX0pYke9q/arcgis/rest/services/Monitoring_Health_20201116/FeatureServer/0', "",
        {},
        {
            token: '9LkHUtPISDQr5aRJTTPXE-zbIWVgkCSqn10q5Xpo_xYc8XDdSijqImR4RbCeGxLlCl6n-UlwOwhnC3KZIqTF2guYdmMySyHzEUFRPFdPgEHK7pl813wBSoAbY8mQBOHE-8iCRvv06i-DfNnJ8Olm6ONOmaF3ms-j1UwZGmw4owDTI6ZDjwFKW0-iEo_vfPau2E_j0LNf0u1t0sZ9cxNL5Z69XLhvPa0UbgA0Ogdh4f-MREFCWg1glT3xpZYu4GC0CeFXDS6hH0zLunkmjUYHmUIv7ttJJCgSMwMaum9P8Tv9hgyXWucysJkNbuLbjr7P'
        },
        'ESRI'
    ],
    [
        'COVID Community Vulnerability', 'https://services3.arcgis.com/7J7WB6yJX0pYke9q/arcgis/rest/services/Somalia_Region_CCVI/FeatureServer/0', "CCVI",
        {},
        {
            token: '9LkHUtPISDQr5aRJTTPXE-zbIWVgkCSqn10q5Xpo_xYc8XDdSijqImR4RbCeGxLlCl6n-UlwOwhnC3KZIqTF2guYdmMySyHzEUFRPFdPgEHK7pl813wBSoAbY8mQBOHE-8iCRvv06i-DfNnJ8Olm6ONOmaF3ms-j1UwZGmw4owDTI6ZDjwFKW0-iEo_vfPau2E_j0LNf0u1t0sZ9cxNL5Z69XLhvPa0UbgA0Ogdh4f-MREFCWg1glT3xpZYu4GC0CeFXDS6hH0zLunkmjUYHmUIv7ttJJCgSMwMaum9P8Tv9hgyXWucysJkNbuLbjr7P'
        },
        'ESRI'
    ],
    [
        'Flood Forecast', 'https://livefeeds2.arcgis.com/arcgis/rest/services/GEOGLOWS/GlobalWaterModel_Medium/MapServer/export', "",
        {
            dpi: 96,
            transparent: true,
            format: 'png32',
            layers: 'show:0',
            time: 'null,null',
            f: 'image'
        },
        {},
        'Raster'
    ],
    [
        'Flood Hazard - Risk 100 Yrp', 'https://db1.unepgrid.ch/geoserver/wms', "",
        {
            SERVICE: 'WMS',
            REQUEST: 'GetMap',
            FORMAT: 'image/png',
            TRANSPARENT: 'TRUE',
            STYLES: '',
            VERSION: '1.1.1',
            LAYERS: 'GAR2015:flood_hazard_100_yrp',
            WIDTH: 1390,
            HEIGHT: 669,
            SRS: 'EPSG:3857',
            _ts: 1638173944415
        },
        {},
        'Raster'
    ]
]