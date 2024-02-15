//Função para obter a lista existente do servidor via requisição GET
const getList = async () => {
  let url = 'http://127.0.0.1:5000/empresas';
  fetch(url, {
    method: 'get',
  })
    .then((response) => response.json())
    .then((data) => {
      data.empresas.forEach(item => insertList(item.nome_empresa, item.nome_fantasia, item.cnpj, item.nome_responsavel, item.telefone, item.email))
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}


//Chamada da função para carregamento inicial dos dados
getList()


//Função para colocar um item na lista do servidor via requisição POST
const postItem = async (inputCompany, inputTradingName, inputCnpj, inputContact, inputPhone, inputEmail) => {
  const formData = new FormData();
  formData.append('nome_empresa', inputCompany);
  formData.append('nome_fantasia', inputTradingName);
  formData.append('cnpj', inputCnpj);
  formData.append('nome_responsavel', inputContact);
  formData.append('telefone', inputPhone);
  formData.append('email', inputEmail);

  let url = 'http://127.0.0.1:5000/empresa';
  fetch(url, {
    method: 'post',
    body: formData
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}


//Função para criar um botão close para cada item da lista
const insertButton = (parent) => {
  let span = document.createElement("span");
  let txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  parent.appendChild(span);
}


//Função para remover um item da lista de acordo com o click no botão close
const removeElement = () => {
  let close = document.getElementsByClassName("close");
  // var table = document.getElementById('myTable');
  let i;
  for (i = 0; i < close.length; i++) {
    close[i].onclick = function () {
      let div = this.parentElement.parentElement;
      const nomeItem = div.getElementsByTagName('td')[0].innerHTML
      if (confirm("Você tem certeza?")) {
        div.remove()
        deleteItem(nomeItem)
        alert("Removido!")
      }
    }
  }
}


//Função para deletar um item da lista do servidor via requisição DELETE
const deleteItem = (item) => {
  console.log(item)
  let url = 'http://127.0.0.1:5000/empresa?nome_empresa=' + item;
  fetch(url, {
    method: 'delete'
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}


//Função para adicionar um novo item com nome, quantidade e valor 
const newItem = () => {
  let inputCompany = document.getElementById("newInput").value;
  let inputTradingName = document.getElementById("newTradingName").value;
  let inputCnpj = document.getElementById("newCnpj").value;
  let inputContact = document.getElementById("newContact").value;
  let inputPhone = document.getElementById("newPhone").value;
  let inputEmail = document.getElementById("newEmail").value;

  let errorMessage = '';

  if (inputCompany === '') {
      errorMessage += "Razão social \n";
  } if (inputTradingName === '') {
      errorMessage += "Nome fantasia \n";
  } if (inputCnpj === '') {
      errorMessage += "CNPJ \n";
  } if (inputContact === '') {
      errorMessage += "Responsável \n";
  } if (inputPhone === '') {
      errorMessage += "Telefone \n";
  } if (inputEmail === '') {
      errorMessage += "E-mail \n";
  } if (errorMessage !== '') {
    alert("Os seguintes campos são obrigatórios:\n" + errorMessage);
  } else {
    insertList(inputCompany, inputTradingName, inputCnpj, inputContact, inputPhone, inputEmail);
    postItem(inputCompany, inputTradingName, inputCnpj, inputContact, inputPhone, inputEmail);
    alert("Item adicionado!");
  }
}


//Função para inserir items na lista apresentada
const insertList = (nameCompany, TradingName, Cnpj, Contact, Phone, Email) => {
  var item = [nameCompany, TradingName, Cnpj, Contact, Phone, Email]
  var table = document.getElementById('myTable');
  var row = table.insertRow();

  for (var i = 0; i < item.length; i++) {
    var cel = row.insertCell(i);
    cel.textContent = item[i];
  }
  insertButton(row.insertCell(-1))
  document.getElementById("newInput").value = "";
  document.getElementById("newTradingName").value = "";
  document.getElementById("newCnpj").value = "";
  document.getElementById("newContact").value = "";
  document.getElementById("newPhone").value = "";
  document.getElementById("newEmail").value = "";

  removeElement()
}