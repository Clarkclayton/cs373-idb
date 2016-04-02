var data = [
    {id: 1, name: "Bulbasaur", type_id_1: 12, type_name_1: "grass", average_stats: 53,
    type_id_2: 4, type_name_2: "poison"},
    {id: 4, name: "Charmander", type_id_1: 10, type_name_1: "fire", average_stats: 52},
    {id: 7, name: "Squirle", type_id_1: 11, type_name_1: "water", average_stats: 52}
];

var PokeRow = React.createClass({
render: function(){
    var pk = this.props.pokemon;
    return(
        <tr>
            <td><a href={"/pokemon/" + pk.id}>
                <img src={"/static/img/pokemon" + pk.id + ".png"}/></a>
            </td>
            <td>{pk.id}</td>
            <td><a href={"/pokemon/" + pk.id}>{pk.name}</a></td>
            <td><a href={"/type/" + pk.type_id_1}>
                <img id="move_type_text_img" src={"/static/img/moves/" + pk.type_name_1 + "_text.png"}/>
            </a></td>
            <td>
            { pk.type_id_2 ?
            <a href={"/type/" + pk.type_id_2}>
                <img id="move_type_text_img" src={"/static/img/moves/" + pk.type_name_2 + "_text.png"}/>
            </a>
            : ""}
            </td>
            <td> {pk.average_stats} </td>
        </tr>)
    }
});

var PokeTable = React.createClass({
render: function(){
    var rowNodes = this.props.data.map(function(pk){
        return (<PokeRow pokemon={pk} key={pk.id}/>)
    });

    return(
        <table className="poke-table sortable-theme-bootstrap" data-sortable>
            <thead>
                <tr>
                    <th data-sortable="false">Sprite</th>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Primary Type</th>
                    <th>Secondary Type</th>
                    <th>Average Stats</th>
                </tr>
            </thead>
            <tbody>
            {rowNodes}
            </tbody>
        </table>)
    }
});

ReactDOM.render(
    <PokeTable data={data}/>,
    document.getElementById('pokediv')
);
