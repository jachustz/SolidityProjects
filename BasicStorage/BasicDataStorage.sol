// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract BasicDataStorage {
    uint256 favoriteNumber;

    struct Transmittal {
        string project;
        uint256 drawingNumber;
        uint256 date;
    }

    Transmittal[] public people;

    mapping(string => uint256) public projectToDrawingNumber;

    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }

    function addPerson(
        string memory _project,
        uint256 _drawingNumber,
        uint256 _date
    ) public {
        require(bytes(_project).length > 0);
        require(_drawingNumber > 0);
        require(_date > 0);
        people.push(Transmittal(_project, _drawingNumber, _date));
        projectToDrawingNumber[_project] = _drawingNumber;
    }
}
