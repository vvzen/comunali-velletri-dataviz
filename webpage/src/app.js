let section_data_csv;
let addedSections;
let sectionPlacesInfo; // used for storing section number
let markers;
// contains all the voting sections infos
let sections = [];


function initMap() {

    let velletri = {
        lat: 41.686667,
        lng: 12.7775
    };

    // load the map
    let map = new google.maps.Map(document.getElementById('map'), {
        zoom: 15,
        center: velletri
    });

    // load all the data for each section
    d3.csv("/data/all_sections_votes.csv", function (data) {

        addedSections = [];
        markers = [];
        sectionPlacesInfo = {};

        section_data_csv = data;

        // loop through each section of the csv
        section_data_csv.forEach(row => {

            let coordinates = {
                lat: parseFloat(row["lat"]),
                lng: parseFloat(row["lng"])
            }

            let sectionName = row["Nome sezione"].toString();

            // create a "section" object similar to the csv:
            // key: the party name, value: the number of votes
            // two additional keys are "Numero sezione" and "Nome sezione"
            let partiesNames = Object.keys(row);
            let votes = Object.values(row);
            let section = {};
            for (let i = 0; i < partiesNames.length; i++) {
                section[partiesNames[i]] = votes[i];
            }
            sections.push(section);

            console.log("sections");
            console.log(sections);

            // add marker only if the place hosting the section
            // isn't already on the map
            if (addedSections.indexOf(sectionName) === -1) {

                addedSections.push(sectionName);

                sectionPlacesInfo[sectionName] = [];
                sectionPlacesInfo[sectionName].push({
                    "section_num": row["Numero sezione"]
                });

                // console.log("here");
                markers.push(
                    new google.maps.Marker({
                        position: coordinates,
                        map: map,
                        section_num: row["Numero sezione"],
                        name: sectionName
                    })
                )
            } else {
                sectionPlacesInfo[sectionName].push({
                    "section_num": row["Numero sezione"]
                });
            }

        });

        // add markers on the map
        markers.forEach(marker => {
            marker.addListener('click', function () {

                let contentString =
                    `<div id="siteNotice">` +
                    `</div>` +
                    `<div id="content">` +
                    `<h3 id="firstHeading" class="firstHeading">${marker.name}</h3>` +
                    `<p><em>Sezioni di voto:</em></p>`;

                console.log(sectionPlacesInfo);

                // add sections for each voting site
                sectionPlacesInfo[marker.name].forEach(place => {
                    console.log(place);
                    contentString += `<li><a href="#" class="section" id='${place.section_num}'>${place.section_num}</a></li>`
                })

                contentString += "</div>";

                let infowindow = new google.maps.InfoWindow({
                    content: contentString
                });

                infowindow.open(map, marker);
            });
        });

        // FIXME: doesn't work
        // add listeners for each section link
        $("a.section").click(function (event) {
            console.log("HERE");
            console.log(`clicked on section ${event.target.id}`);
        });
    });
}

function test(sectionNum) {

    // find the related section in the sections array
    let matchingSection = sections.filter(function (obj) {
        return obj["Numero sezione"] == sectionNum;
    });

    console.log(matchingSection);
    return matchingSection;
}