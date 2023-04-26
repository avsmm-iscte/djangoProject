import React from 'react';
function Header() { //(8)
 return ( //(9)
 <>
 <div className="text-center">
 <img
 src="https://keystoneacademicres.cloudinary.com/image/upload/q_auto,f_auto,w_743,c_limit/element/1
1/111948_2.jpg"
 width="300"
 alt="ISCTE"
 className="img-thumbnail"
 style={{ marginTop: "20px" }} //(10)
 />
 <br />
 <br />
 <h5>
 <i>Desenvolvimento para a Internet e Aplicações Móveis (LEI
e LIGE)</i>
 </h5>
 <br />
 <hr />
 <br />
 <h2>Exemplo de integração de Django com React</h2>
 <br />
 </div>
 </> //(9)
 );
}
export default Header;