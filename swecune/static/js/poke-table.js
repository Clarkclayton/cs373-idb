var data = [
    {id: 1, name: "Bulbasaur", type_id_1: 12, type_name_1: "grass", average_stats: 53,
    type_id_2: 4, type_name_2: "poison"},
    {id: 4, name: "Charmander", type_id_1: 10, type_name_1: "fire", average_stats: 52},
    {id: 7, name: "Squirle", type_id_1: 11, type_name_1: "water", average_stats: 52},
    {id: 1, name: "Bulbasaur", type_id_1: 12, type_name_1: "grass", average_stats: 53,
    type_id_2: 4, type_name_2: "poison"},
    {id: 4, name: "Charmander", type_id_1: 10, type_name_1: "fire", average_stats: 52},
    {id: 7, name: "Squirle", type_id_1: 11, type_name_1: "water", average_stats: 52},
    {id: 1, name: "Bulbasaur", type_id_1: 12, type_name_1: "grass", average_stats: 53,
    type_id_2: 4, type_name_2: "poison"},
    {id: 4, name: "Charmander", type_id_1: 10, type_name_1: "fire", average_stats: 52},
    {id: 7, name: "Squirle", type_id_1: 11, type_name_1: "water", average_stats: 52},
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

var k = 0;

var SLICE_WIDTH = 4;

var PokeTable = React.createClass({
getInitialState: function(){
        return ({
            rowNodes: this.props.data.slice(0, SLICE_WIDTH).map(function(pk){
                k++;
                return (<PokeRow pokemon={pk} key={k}/>)
            })
        })
    },

changePage: function(page){
        console.log("page: " + page);
        this.setState({
            rowNodes: this.props.data.slice((page-1) * SLICE_WIDTH, page * SLICE_WIDTH).map(function(pk){
                k++;
                return (<PokeRow pokemon={pk} key={k}/>)
            })
        })
    },

render: function(){
    return(
        <div>
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
            {this.state.rowNodes}
            </tbody>
        </table>
        <PokePage p={this}/>
        </div>)
    }
});

var handleClick = function(table, page){
    console.log(table);
    table.changePage(page);
}

var PokePage = React.createClass({
render: function(){
    return(
        <nav>
           <ul className="pagination">
               <li>
                   <a href="#" aria-label="Previous">
                   <span aria-hidden="true">&laquo;</span>
                   </a>
               </li>
               <li><a href="#" onClick={handleClick.bind(this, this.props.p, 1)}>1</a></li>
               <li><a href="#" onClick={handleClick.bind(this, this.props.p, 2)}>2</a></li>
               <li><a href="#" onClick={handleClick.bind(this, this.props.p, 3)}>3</a></li>
               <li><a href="#" onClick={handleClick.bind(this, this.props.p, 4)}>4</a></li>
               <li><a href="#" onClick={handleClick.bind(this, this.props.p, 5)}>5</a></li>
               <li>
                   <a href="#" aria-label="Next">
                   <span aria-hidden="true">&raquo;</span>
                   </a>
               </li>
           </ul>
        </nav>)
    }
});

ReactDOM.render(
    <PokeTable data={data}/>,
    document.getElementById('pokediv')
);
